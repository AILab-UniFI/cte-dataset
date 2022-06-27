import json
from src.paths import MERGED, PUB1M, PUBLAY
from src.data.merged import *
from src.data.publaynet import *
from src.data.pubtables1m import *
from src.const import categories_colors
from src.utils import print_annotations
from utils import project_tree

"""
        The data folder must be like follow:
*       data/
*           publaynet/
?               PubLayNet_PDF/  <- downloaded from PubLayNet github repo
?               test.json   <- annotations
?               train.json  <- annotations
?               val.json    <- annotations
*           pubtables-1m/
?               PubTables1M-PDF-Annotations-JSON/   <- downloaded from PubTables-1M github repo
*           merged/
!               test.json   <- We'll create this here  (pubtab-1m + publaynet)
!               train.json  <- We'll create this here  (pubtab-1m + publaynet)
!               val.json    <- We'll create this here  (pubtab-1m + publaynet)
""" 

####################
#* MAIN
####################

if __name__ == "__main__":

    # generate project tree
    project_tree()
    
    SPLITS = ["test", "val", "train"]
    debug = False # set to False to do not print annotation examples

    for phase, split in enumerate(SPLITS):

        print("")
        print(f"Processing {split}:")

        ### PATHS ###

        publay_annotations = PUBLAY / f"{split}.json"  # PubLayNet Annotations
        pub1m_annotations = PUB1M  # PubTable-1M Annotations
        final_annotations = MERGED / f"{split}.json"  # final json to be used

        ### PubLayNet processing ###

        papers, pages_idx = pln_preprocess(publay_annotations)
        num_tables = pln_filter_tables(papers, pages_idx)

        ### PubTable-1M processing ###

        split_dict = pt1m_preprocess(papers, pub1m_annotations)

        ### MERGE processing ###
        
        differences = diff_pln_pt1m(num_tables, split_dict)
        todiscard = get_not_annotated_tables(differences)
        refactored_papers = merge_annotations(papers, pages_idx, split_dict, todiscard)
        objects, tokens, links = parse_pdf(refactored_papers, split)

        ### End file -> saving ###
        # {"id": 0, "name": "OTHER", "color": (127, 127, 127)},
        refactored_dict = {
            "categories": [{'id':category.value, 'name': category.name, 'color': categories_colors[category.value] } for category in Categories_names],
            "objects": objects,
            "tokens": tokens,
            "links": links
        }

        with open(final_annotations, "w") as f:
            f.write(json.dumps(refactored_dict))
        
        if debug:
            with open(final_annotations, "r") as ann:
                annotations = json.load(ann)
                print_annotations(annotations, split)
