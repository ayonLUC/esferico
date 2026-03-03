import pandas as pd

DATA_PATH = "data/EPL24_25.csv"

def load_matches(path: str = DATA_PATH):
    df = pd.read_csv(path)
    return df