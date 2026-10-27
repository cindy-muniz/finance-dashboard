import pandas as pd

def add_month_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'month_year' column for grouping by month (e.g. '2024-03').
    """
    df = df.copy()
    df["month_year"] = df["date"].dt.to_period("M").astype(str)
    return df


def monthly_spending_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns total spending per category per month.
    """
    return (
        df.groupby(["month_year", "category"])["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_spent"})
        .sort_values(["month_year", "total_spent"], ascending=[True, False])
    )


def total_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns overall total spending per category across all time.
    """
    return (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_spent"})
        .sort_values("total_spent", ascending=False)
    )


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns total spending per month across all categories.
    """
    return (
        df.groupby("month_year")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_spent"})
        .sort_values("month_year")
    )


def flag_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """
    Flags transactions that are unusually large within their category.
    A transaction is flagged if it exceeds the category mean by
    'threshold' standard deviations (z-score method).
    """
    df = df.copy()
    df["is_anomaly"] = False

    for category in df["category"].unique():
        mask = df["category"] == category
        category_data = df.loc[mask, "amount"]
        mean = category_data.mean()
        std = category_data.std()

        if std > 0:
            z_scores = (category_data - mean) / std
            df.loc[mask, "is_anomaly"] = z_scores > threshold

    return df


if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from pipeline.ingest import load_transactions

    # Load data
    base_dir = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, "data", "transactions.csv")
    df = load_transactions(filepath)

    # Run transformations
    df = add_month_year(df)
    df = flag_anomalies(df)

    print("=== Monthly Spending by Category (first 10 rows) ===")
    print(monthly_spending_by_category(df).head(10))

    print("\n=== Total by Category ===")
    print(total_by_category(df))

    print("\n=== Monthly Totals ===")
    print(monthly_totals(df))

    print("\n=== Flagged Anomalies ===")
    anomalies = df[df["is_anomaly"] == True]
    print(f"Found {len(anomalies)} anomalous transactions:")
    print(anomalies[["transaction_id", "date", "category", "amount"]])