from pathlib import Path
from dotenv import dotenv_values
import os

# ROOT
HERE = Path(os.path.dirname(os.path.abspath(__file__)))
config = dotenv_values(HERE / "root.env")
ROOT = Path(config['ROOT'])

# DATA
DATA = ROOT / 'data'
PUBLAY = DATA / 'publaynet'
PUB1M = DATA / 'pubtables-1m'
MERGED = DATA / 'merged'

# BASELINES
BASELINES = ROOT / 'baselines'
