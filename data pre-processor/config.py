NAME = "pre-processed dataset"
SOURCE = "dataset/raw_dataset"
DESTINATION = "dataset"
UPPER_JAW_DIR = "Labels_Upper jaw"
LOWER_JAW_DIR = "Labels_Lower jaw"
MAX_DIM = 512
LABELS = [
    "tooth",
    "non-carious lesion",
    "staining or visible changes without cavitation",
    "calculus",
    "visible changes with microcavitation", 
    "visible changes with cavitation",
    ]