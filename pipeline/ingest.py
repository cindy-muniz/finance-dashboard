import pandas as pd
import os

EXPECTED_COLUMNS = {"transaction_id", "date", "category", "amount", "description"}

def load_transactions(filepath: str) -> pd.DataFrame:
    """
    Loads transaction CSV file and validates its structure.
    Returns a cleaned DataFrame ready for transformation.
    """
    # Check file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    # Load CSV
    df = pd.read_csv(filepath)

    # Validate columns
    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    # Drop rows where amount or date is missing
    before = len(df)
    df = df.dropna(subset=["amount", "date"])
    after = len(df)
    if before != after:
        print(f"Warning: Dropped {before - after} rows with missing data")

    # Convert date column to datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Convert amount to float
    df["amount"] = df["amount"].astype(float)

    # Remove any duplicate transaction IDs
    df = df.drop_duplicates(subset=["transaction_id"])

    print(f"Successfully loaded {len(df)} transactions")
    return df


if __name__ == "__main__":
    # Build path to transactions.csv relative to project root
    base_dir = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, "data", "transactions.csv")

    df = load_transactions(filepath)
    print(df.dtypes)
    print(df.head())