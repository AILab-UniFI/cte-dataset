import os
from paths import *

def create_folder(folder_path : str):
    """create a folder if not exists

    Args:
        folder_path (str): path
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

def project_tree():
    create_folder(DATA)
    create_folder(PUBLAY)
    create_folder(PUB1M)
    create_folder(MERGED)
    create_folder(BASELINES)
    return