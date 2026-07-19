import json
import os

# Get the directory where this file is located
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(DATA_DIR, "celestial_bodies.json")

# Load the JSON data
with open(JSON_FILE, "r") as f:
    BODY_DATA = json.load(f)