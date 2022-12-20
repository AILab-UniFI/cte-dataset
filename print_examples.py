import random
import json
from pdf2image import convert_from_path
from PIL import ImageDraw
from src.paths import PUBLAY, MERGED
from src.const import categories_colors, Categories_names
from src.utils import create_folder

def visualize(stats=False):

    #? COUNTING DATASET STATISTICS
    if stats:
        for split in ['test', 'train', 'val']:
                annotations_path = MERGED / f'{split}.json'
                pages = 0
                tables = 0
                with open(annotations_path, "r") as ann:
                        annotations = json.load(ann)
                for page, objects in  annotations['objects'].items():
                        pages += 1
                        tables += len([object for object in objects if object[2] == Categories_names.TABLE.value])

                print(f"{split}: # pages {pages} - # tables {tables}")
    
    #? CHOOSING A RANDOM SAMPLE TO VISUALIZE FROM THE TESTSET

    SPLIT = 'test' # choose between train, dev (val), test
    annotations_path = MERGED / f'{SPLIT}.json'
    with open(annotations_path, "r") as ann:
        annotations = json.load(ann)

    data = PUBLAY / 'PubLayNet_PDF' / SPLIT
    pdf_name = random.choice(list(annotations['objects']))
    pdf_path = data / pdf_name

    print(f'Visualizing {pdf_name}')

    #? EXTRACTING OBJECTS, TOKENS AND LINKS

    objects = annotations['objects'][pdf_name]
    print(objects)

    pdf_img = convert_from_path(pdf_path)[0]
    draw = ImageDraw.Draw(pdf_img)
    for object in objects:
        draw.rectangle(object[1], fill=tuple(categories_colors[object[2]]), outline='black', width=4)
    pdf_img.save('visualization/objects.png')

    tokens = annotations['tokens'][pdf_name]

    pdf_img = convert_from_path(pdf_path)[0]
    draw = ImageDraw.Draw(pdf_img)

    for token in tokens:
        draw.rectangle(token[1], fill=tuple(categories_colors[token[3]]), outline='black', width=4)
    pdf_img.save('visualization/tokens.png')

    links = annotations['links'][pdf_name]

    #? PRINTING EXAMPLES ON VISUALIZATION FOLDER

    if links:

            # GRID CELLS

            pdf_img = convert_from_path(pdf_path)[0]
            draw = ImageDraw.Draw(pdf_img)

            for token in tokens:
                    draw.rectangle(token[1], fill='black')

            for link in links:
                    if link[1] == Categories_names.TABLE_GCELL.value:
                            bbox = [min([t[1][0] for t in tokens if t[0] in link[2]]), min([t[1][1] for t in tokens if t[0] in link[2]]),
                                    max([t[1][2] for t in tokens if t[0] in link[2]]), max([t[1][3] for t in tokens if t[0] in link[2]]),]
                            draw.rectangle(bbox, fill=tuple(categories_colors[link[1]]), outline='black', width=4)
            pdf_img.save('visualization/grids.png')

            # ROWS

            pdf_img = convert_from_path(pdf_path)[0]
            draw = ImageDraw.Draw(pdf_img)

            for token in tokens:
                    draw.rectangle(token[1], fill='black')

            for link in links:
                    if link[1] == Categories_names.TABLE_ROW.value:
                            bbox = [min([t[1][0] for t in tokens if t[0] in link[2]]), min([t[1][1] for t in tokens if t[0] in link[2]]),
                                    max([t[1][2] for t in tokens if t[0] in link[2]]), max([t[1][3] for t in tokens if t[0] in link[2]]),]
                            draw.rectangle(bbox, fill=tuple(categories_colors[link[1]]), outline='black', width=4)
            pdf_img.save('visualization/rows.png')

            # COLUMNS

            pdf_img = convert_from_path(pdf_path)[0]
            draw = ImageDraw.Draw(pdf_img)

            for token in tokens:
                    draw.rectangle(token[1], fill='black')

            for link in links:
                    if link[1] == Categories_names.TABLE_COL.value:
                            bbox = [min([t[1][0] for t in tokens if t[0] in link[2]]), min([t[1][1] for t in tokens if t[0] in link[2]]),
                                    max([t[1][2] for t in tokens if t[0] in link[2]]), max([t[1][3] for t in tokens if t[0] in link[2]]),]
                            draw.rectangle(bbox, fill=tuple(categories_colors[link[1]]), outline='black', width=4)
            pdf_img.save('visualization/columns.png')


create_folder('visualization')
visualize()