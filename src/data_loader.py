import pandas as pd

DATA_PATH = "data/EPL24_25.csv"

KEEP_COLS = ["Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]

def load_matches(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Keep only relevant columns (ignore missing ones safely)
    cols = [c for c in KEEP_COLS if c in df.columns]
    df = df[cols].copy()

    return df