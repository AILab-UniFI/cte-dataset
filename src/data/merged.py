from math import inf
from tqdm import tqdm
import fitz
import time
from src.const import SCALE_FACTOR, Categories_names
from src.paths import PUBLAY

####################
#! MERGED Dataset
####################

def diff_pln_pt1m(num_tables_dict, split_dict, debug=False):
        
    paper_diffs_table_numbers = dict()

    counter: dict = {
        "all": 0,
        "partial": 0,
        "null": 0,
        "notab": 0,
    }

    for file_name, file_dict_from_pln in tqdm(num_tables_dict.items(), desc=" - evaluate differences"):

        file_dict_from_pt1m = split_dict[file_name]

        for page_number_pln, tables_number_pln in file_dict_from_pln.items():

            if tables_number_pln == 0:
                if debug: counter["notab"] += 1
                continue

            tables_number_pt1m = list(file_dict_from_pt1m.get(page_number_pln, {"err": "err"}).values())
            if tables_number_pt1m[0] == "err":
                tables_number_pt1m = 0
            else:
                tables_number_pt1m = len(tables_number_pt1m)
            paper_dict = paper_diffs_table_numbers.get(file_name, {})
            paper_dict[page_number_pln] = [tables_number_pln, tables_number_pt1m]
            paper_diffs_table_numbers[file_name] = paper_dict

            if debug:
                if tables_number_pt1m == 0:
                    counter["null"] += 1
                elif tables_number_pln > tables_number_pt1m:
                    counter["partial"] += 1
                elif tables_number_pln == tables_number_pt1m:
                    counter["all"] += 1
                else: raise ValueError("Error")

    if debug:
        print('all', counter['all'])
        print('partial', counter['partial'])
        print('null', counter['null'])
        print('notab', counter['notab'])

    return paper_diffs_table_numbers

def get_not_annotated_tables(differences):
    todiscard = dict()
    for paper, pages in differences.items():
        for page, counts in pages.items():
            if counts[0] != counts[1]:  # if [tables_in_page] != [tables_annotated]
                todiscard[paper + "_" + str(page).zfill(5) + ".jpg"] = False
    return todiscard

# todo: very slow, list -> ?
# todo: change magic number -> Enum
def get_caption(rectA, rects):

    distances = []
    for rectB in rects:

        if rectA == rectB: continue

        if rectA[0][0] < rectB[0][2] and rectB[0][0] < rectA[0][2]:
            
            if rectA[1] == Categories_names.TABLE.value:
                distances.append([rectA[0][1] - rectB[0][3], rects.index(rectB)])
            
            if rectA[1] == Categories_names.FIGURE.value:
                distances.append([rectA[0][3] - rectB[0][1], rects.index(rectB)])

    if rectA[1] == Categories_names.TABLE.value:
        pos_dist = [d for d in distances if d[0] > 0]
        if pos_dist:
            closer_rect = min(pos_dist)[1]
            rects[closer_rect][1] = Categories_names.CAPTION.value
            rects[closer_rect][2] = Categories_names.CAPTION.name
            
    elif rectA[1] == Categories_names.FIGURE.value:
        neg_dist = [d for d in distances if d[0] < 0]
        if neg_dist:
            closer_rect = max(neg_dist)[1]
            rects[closer_rect][1] = Categories_names.CAPTION.value
            rects[closer_rect][2] = Categories_names.CAPTION.name

    return rects

# todo: very slow, list -> ?
# todo: change magic number -> Enum
def add_caption(new_annotations):

    tables = [elem for elem in new_annotations if elem[1] == Categories_names.TABLE.value] # 4 <- tables
    if tables:
        for t in tables:
            new_annotations = get_caption(t, new_annotations)
    images = [elem for elem in new_annotations if elem[1] == Categories_names.FIGURE.value] # 5 <- images
    if images:
        for i in images:
            new_annotations = get_caption(i, new_annotations)
    return new_annotations

# todo: change magic number -> Enum
# todo: multiple nested loops
def merge_annotations(papers, pages_idx, split_dict, todiscard):
    refactored_papers = dict()
    # refactoring annotations, adding table information
    for paper, infos in tqdm(papers.items(), desc=" - refactoring"):
        for key, value in infos.items():
            # get pages
            if key == "pages":
                current_pages_index = []
                for page in value:
                    if todiscard.get(page, True):
                        current_pages_index.append(pages_idx[page])
                        app = refactored_papers.get(paper, {"pages": [], "annotations": []})
                        app["pages"].append(page.split(".")[0] + ".pdf")
                        refactored_papers[paper] = app

            # get annotations
            if key == "annotations" and len(current_pages_index) != 0:
                new_annotations = []
                previous_id = current_pages_index[0]
                for ann in value:
                    if ann["image_id"] in current_pages_index:
                        if ann["image_id"] != previous_id:
                            new_annotations = add_caption(new_annotations)
                            refactored_papers[paper]["annotations"].append(new_annotations)
                            new_annotations = []
                            previous_id = ann["image_id"]
                        ann["bbox"][2] += ann["bbox"][0]
                        ann["bbox"][3] += ann["bbox"][1]
                        if ann["category_id"] == Categories_names.TEXT.value:  # text
                            new_annotations.append([
                                [int(a / SCALE_FACTOR) for a in ann["bbox"]], 
                                Categories_names.TEXT.value, 
                                Categories_names.TEXT.name, 
                                None, None, None])

                        elif ann["category_id"] == Categories_names.TITLE.value:  # title
                            new_annotations.append([
                                [int(a / SCALE_FACTOR) for a in ann["bbox"]],
                                Categories_names.TITLE.value, 
                                Categories_names.TITLE.name, 
                                None, None, None])
                        
                        elif ann["category_id"] == Categories_names.LIST.value:  # list
                            new_annotations.append([
                                [int(a / SCALE_FACTOR) for a in ann["bbox"]], 
                                Categories_names.LIST.value, 
                                Categories_names.LIST.name, 
                                None, None, None])
                        
                        elif ann["category_id"] == Categories_names.TABLE.value:  # table
                            new_annotations.append([
                                [int(a / SCALE_FACTOR) for a in ann["bbox"]], 
                                Categories_names.TABLE.value, 
                                Categories_names.TABLE.name, 
                                None, None, None])
                        
                        elif ann["category_id"] == Categories_names.FIGURE.value:  # figure
                            new_annotations.append([
                                [int(a / SCALE_FACTOR) for a in ann["bbox"]], 
                                Categories_names.FIGURE.value, 
                                Categories_names.FIGURE.name, 
                                None, None, None])

                new_annotations = add_caption(new_annotations)
                refactored_papers[paper]["annotations"].append(new_annotations)

    for paper, infos in tqdm(split_dict.items(), desc=" - adding table information"):
        if paper in refactored_papers.keys():
            pages = [int(page.split(".")[0].split("_")[1]) for page in refactored_papers[paper]["pages"]]
            if infos:
                for num_page, table in infos.items():
                    if int(num_page) in pages:
                        paper_anns_page = refactored_papers[paper]["annotations"][pages.index(int(num_page))]
                        for _, cells in table.items():
                            for cell in cells:
                                cell = list(cell)
                                cell[0] = [int(a / SCALE_FACTOR) for a in cell[0]]
                                paper_anns_page.append(cell)
                        refactored_papers[paper]["annotations"][pages.index(int(num_page))] = paper_anns_page
    return refactored_papers

def parse_pdf(refactored_papers, split):
    if split == 'val': split = 'dev'
    all_pdf = PUBLAY / f'PubLayNet_PDF/{split}'
    objects, tokens, links = {}, {}, {}
    for paper in tqdm(refactored_papers.keys(), desc = " - final annotations"):
        for id, annotations in enumerate(refactored_papers[paper]['annotations']):
            page = refactored_papers[paper]['pages'][id]
            objs = get_objects(annotations)
            tkns = get_tokens(all_pdf / page, annotations, objs)
            if tkns != None:
                objects[page] = objs
                tokens[page] = tkns

    return objects, tokens, links

def center(rect):
    return [int(rect[2]-(rect[2]-rect[0])/2), int(rect[3]-(rect[3]-rect[1])/2)]

def get_tokens(page, annotations, objects):

    def get_label(rectNode):
        """Intersect PyMuPDF elements with annotations to get labels
        """
        
        ref = -1 # reference object to which the token belongs
        label = 0 # class 'OTHER' with no matches
        centerNode = center(rectNode)

        for o in objects:
            rectObj = o[1]
            if (centerNode[0] > rectObj[0] and centerNode[0] < rectObj[2] and centerNode[1] > rectObj[1] and centerNode[1] < rectObj[3]):
                ref = o[0]
        
        for a in annotations:
            if a[2] in ['TABLE', 'TABLE_GCELL', 'TABLE_COL', 'TABLE_ROW']:
                continue #! skip not used classes
            rectAnn = a[0]
            if (centerNode[0] > rectAnn[0] and centerNode[0] < rectAnn[2] and centerNode[1] > rectAnn[1] and centerNode[1] < rectAnn[3]):
                label = a[1]
                if a[2] == 'FIGURE': label = -1
                break
                
        return label, ref

    tokens = []
    
    try:
        doc = fitz.open(page)
    except fitz.fitz.EmptyFileError:
        return None
    p = doc[0]
    
    ### creating node features ###
            
    words = p.get_text("words")
    
    tid = 0
    for a in objects:
        if a[2] == Categories_names.FIGURE.value:
            tokens.append([tid, a[1], "FIGURE", a[2], a[0]])
            tid += 1
    
    prev = False # used for class 'others'
    other_words = [] # used for class 'others'
    for w, word in enumerate(words):
        
        bbox = [int(word[0]/SCALE_FACTOR), 
                int(word[1]/SCALE_FACTOR),
                int(word[2]/SCALE_FACTOR),
                int(word[3]/SCALE_FACTOR)]
        
        label, ref = get_label(bbox)

        if label == -1:
            continue
        
        # counting 'other' words to group them into objects later
        if ref == -1 and not prev:
            start = w
            prev = True
        elif ref != -1 and prev:
            other_words.append([start, w])
            prev = False

        tokens.append([tid, bbox, word[4], label, ref])
        tid += 1

    # add class 'other' to objects
    for interval in other_words:
        other_bbox = [inf, inf, 0, 0]
        for token in tokens[interval[0]:interval[1]]:
            token[4] = len(objects)
            other_bbox = [min(token[1][0], other_bbox[0]), 
                        min(token[1][1], other_bbox[1]), 
                        max(token[1][2], other_bbox[2]), 
                        max(token[1][3], other_bbox[3])]
        objects.append([len(objects), other_bbox, 0])
    
    return tokens

def get_objects(annotations):
    objects = []
    for num, ann in enumerate(annotations):
        if ann[2] in ['TABLE_TCELL', 'TABLE_GCELL', 'TABLE_COL', 'TABLE_ROW', 'TABLE_COLH', 'TABLE_SP']:
            num -= 1
            continue
        else:
            objects.append([num, ann[0], ann[1]])
    return objects
