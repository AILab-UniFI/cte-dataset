from pathlib import Path
from dotenv import dotenv_values
import os

config = dotenv_values("root.env")
ROOT = Path(config['ROOT'])

# DATA
DATA = ROOT / 'data'
PUBLAY = DATA / 'publaynet'
PUB1M = DATA / 'pubtables-1m/PubTables1M-PDF-Annotations-JSON'
MERGED = DATA / 'merged'

# BASELINES
BASELINES = ROOT / 'baselines'
