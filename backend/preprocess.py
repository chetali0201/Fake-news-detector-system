"""Dataset loading, text cleaning and train/validation/test splitting."""
import html
import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42
URL_RE = re.compile(r"https?://\S+|www\.\S+")
TAG_RE = re.compile(r"<[^>]+>")
# Kaggle "True.csv" articles start with "CITY (Reuters) -": a source leak, not real signal.
AGENCY_RE = re.compile(r"^[^()\-]{0,60}\(reuters\)\s*-?\s*", re.IGNORECASE)


def clean_text(text) -> str:
    """Lowercase; strip HTML tags, URLs, punctuation and extra whitespace."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = AGENCY_RE.sub("", text.strip())
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def _read_raw(path: Path) -> pd.DataFrame:
    """Accept a CSV file, or a folder holding news.csv or Fake.csv + True.csv."""
    if path.is_file():
        return pd.read_csv(path)
    if (path / "news.csv").exists():
        return pd.read_csv(path / "news.csv")
    if (path / "Fake.csv").exists() and (path / "True.csv").exists():
        fake = pd.read_csv(path / "Fake.csv").assign(label="FAKE")
        real = pd.read_csv(path / "True.csv").assign(label="REAL")
        return pd.concat([fake, real], ignore_index=True)
    raise FileNotFoundError(
        f"No dataset found at '{path}'. Put news.csv (text,label) or Fake.csv + True.csv "
        "in the data/ folder. See data/README.md."
    )


def load_and_clean(path) -> pd.DataFrame:
    """Return a DataFrame with columns: content (cleaned text), label (FAKE/REAL)."""
    df = _read_raw(Path(path))
    df.columns = [c.strip().lower() for c in df.columns]
    if "label" not in df.columns or not ({"text", "title"} & set(df.columns)):
        raise ValueError("CSV needs a 'label' column and a 'text' and/or 'title' column.")
    print("Missing values per column:\n", df.isna().sum().to_string())
    n0 = len(df)
    df = df.drop_duplicates()
    # Combine title + article when both exist
    parts = [df[c].fillna("") for c in ("title", "text") if c in df.columns]
    df["content"] = (parts[0] + " " + parts[1]).map(clean_text) if len(parts) == 2 else parts[0].map(clean_text)
    df["label"] = df["label"].astype(str).str.strip().str.upper()
    df = df[df["label"].isin(["FAKE", "REAL"]) & (df["content"].str.len() > 0)]
    df = df.drop_duplicates(subset="content")
    print(f"Rows: {n0} -> {len(df)} after removing duplicates/empty/invalid labels")
    print(df["label"].value_counts().to_string())
    return df[["content", "label"]].reset_index(drop=True)


def prepare_splits(df: pd.DataFrame):
    """Stratified 64/16/20 train/validation/test split (same seed => same split everywhere)."""
    X_tmp, X_test, y_tmp, y_test = train_test_split(
        df["content"], df["label"], test_size=0.2, stratify=df["label"], random_state=SEED)
    X_train, X_val, y_train, y_val = train_test_split(
        X_tmp, y_tmp, test_size=0.2, stratify=y_tmp, random_state=SEED)
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)
