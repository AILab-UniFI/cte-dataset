# Contextualized Table Extraction Dataset
- [Contextualized Table Extraction Dataset](#contextualized-table-extraction-dataset)
    - [Dataset Numbers](#dataset-numbers)
    - [A couple of examples](#a-couple-of-examples)
  - [Init](#init)
  - [Project Tree](#project-tree)
  - [Config File Format](#config-file-format)
  - [Cite this project](#cite-this-project)

We have build a dataset for Contextualized Table Extraction fusing to well known datasets:
- [PubLayNet](https://developer.ibm.com/exchanges/data/all/publaynet/)[^1], a dataset for Document Layout Analysis with 5 different labeld regions
- [PubTables-1M](https://msropendata.com/datasets/505fcbe3-1383-42b1-913a-f651b8b712d3)[^2], a dataset to perform Table Detection, Table Structure Recognition and Functional Analysis.

Tables are really important sources of information for research purposes, and giving them a context (instead of just focusing on them) can help in their extraction. We have been inspired by mainly to works:
- [DocBank](https://doc-analysis.github.io/docbank-page/index.html)[^3], to reformulate the problem as a token-classification task
- AxCell[^4], to give table a context also for comparable resarch porpuses

You can read more details in our paper: `Contextualized Table Extraction Dataset`

---

### Dataset Numbers
<img src="imgs/table.png" width="1000" />

---

### A couple of examples
<p>
  <img src="imgs/annotations_00.jpg" width="300" />
  <img src="imgs/annotations_00_table.jpg" width="300" /> 
  <img src="imgs/annotations_00_cells.jpg" width="300" />
</p>

[^1]: Xu Zhong et al., PubLayNet: largest dataset ever for document layout analysis, ICDAR 2019.
[^2]: B. Smock et al., "Towards a universal dataset and metrics for training and evaluating table extraction models", arXiv, November 2021.
[^3]: Li, Minghao, et al. "DocBank: A benchmark dataset for document layout analysis." arXiv preprint arXiv:2006.01038 (2020).
[^4]: Kardas, Marcin, et al. "Axcell: Automatic extraction of results from machine learning papers." arXiv preprint arXiv:2004.14356 (2020)

---

## Init
Run in your environment:
```
python init.py
```
to install dependencies and create the project tree.

Then, download annotations and baselines from `here`.

If you need the data, download them directly from their sites.

## Project Tree
```
  ├── init.py - Initialization script
  ├── generate_annotations.py - Annotation json files generation 
  ├── visualization.ipynb - Visualize annotations on example images
  │
  ├── data/ - where papers are stored
  │   ├── publaynet/ - abstract base class for data loaders
  │   ├── pubtables-1m/ - abstract base class for models
  │   └── merged/ - abstract base class for trainers
  │       ├── region_annotations.json - bigger regions of the page in terms of bounding boxes
  │       └── token_annotations.json - token bounding boxes, textual content and links.
  │
  ├── baselines/ - weights of baseline models
  ├── imgs / - examples
  ```

## Config File Format
Config files are in `.json` format. Example:
```
"papers": {
        "PMC3503280": {
            "pages": [
                "PMC3503280_00001.pdf",
                "PMC3503280_00000.pdf"
            ],
            "annotations": [
                [
                    [
                        [
                            140,
                            1907,
                            808,
                            2063
                        ],
                        1,
                        "TEXT",
                        null,
                        null,
                        null
                    ],
```

## Cite this project
If you want to use our dataset in your project[^1], please cite us:
```
@inproceedings{neumann-etal-2019-scispacy,
    title = "CTE: Contextualized Table Extraction Dataset",
    author = "Gemelli, Andrea  and
      Vivoli, Emanuele",
    abstract = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
}
```
