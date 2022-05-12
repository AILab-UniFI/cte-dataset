import os

if __name__ == "__main__":

    # setting root folder path
    HERE = os.path.dirname(os.path.abspath(__file__))
    with open("root.env", "w") as f:
        f.write(f"ROOT = '{HERE}'")
    
    # generate project tree
    from utils import project_tree
    project_tree()

    # install requirements
    os.system("pip install -r requirements.txt")