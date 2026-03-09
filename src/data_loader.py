import pandas as pd

DATA_PATH = "data/EPL24_25.csv"

KEEP_COLS = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HS",
    "AS",
    "HST",
    "AST"
]

def load_matches(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Fix date format
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True).dt.strftime("%m/%d/%Y")


    cols = [c for c in KEEP_COLS if c in df.columns]
    df = df[cols].copy()

    return df