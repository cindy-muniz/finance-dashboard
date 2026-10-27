import pandas as pd
import random
from datetime import datetime, timedelta

# Settings
NUM_TRANSACTIONS = 200
START_DATE = datetime(2024, 1, 1)

CATEGORIES = [
    "Groceries", "Rent", "Transport", "Dining Out",
    "Entertainment", "Utilities", "Healthcare", "Shopping"
]

CATEGORY_RANGES = {
    "Groceries":     (20, 120),
    "Rent":          (800, 1500),
    "Transport":     (10, 60),
    "Dining Out":    (10, 80),
    "Entertainment": (10, 100),
    "Utilities":     (50, 200),
    "Healthcare":    (20, 300),
    "Shopping":      (15, 250),
}

# Deliberately large purchases, far above each category's normal range, so that
# flag_anomalies has something to find. Uniform random amounts alone can never
# reach a z-score of 2 (max is about 1.73).
OUTLIERS = [
    ("Dining Out", 450.00, "Group birthday dinner"),
    ("Shopping",   1800.00, "New laptop"),
    ("Healthcare", 2500.00, "Emergency room visit"),
]

random.seed(42)

def generate_transactions(n=NUM_TRANSACTIONS):
    transactions = []
    for i in range(n):
        category = random.choice(CATEGORIES)
        low, high = CATEGORY_RANGES[category]
        amount = round(random.uniform(low, high), 2)
        date = START_DATE + timedelta(days=random.randint(0, 364))
        transactions.append({
            "transaction_id": i + 1,
            "date": date.strftime("%Y-%m-%d"),
            "category": category,
            "amount": amount,
            "description": f"{category} purchase #{i + 1}"
        })
    # Added after the loop so the 200 normal rows stay identical to before
    for category, amount, description in OUTLIERS:
        date = START_DATE + timedelta(days=random.randint(0, 364))
        transactions.append({
            "transaction_id": len(transactions) + 1,
            "date": date.strftime("%Y-%m-%d"),
            "category": category,
            "amount": amount,
            "description": description
        })
    return pd.DataFrame(transactions).sort_values(["date", "transaction_id"]).reset_index(drop=True)

if __name__ == "__main__":
    df = generate_transactions()
    import os
    # Write next to this script (data/), regardless of the working directory
    df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions.csv"), index=False)
    print(f"Generated {len(df)} transactions")
    print(df.head(10))