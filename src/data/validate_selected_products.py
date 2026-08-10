import pandas as pd
from pathlib import Path


DATA_FILE = Path(
    "data/processed/selected_products.csv"
)


def validate_dataset():

    print("========================================")
    print("EthicCart Selected Dataset Validation")
    print("========================================")

    df = pd.read_csv(DATA_FILE)

    print(f"\nTotal rows: {len(df):,}")

    # --------------------------------------------------
    # 1. Check product-type distribution
    # --------------------------------------------------

    print("\nProduct type distribution:")

    print(
        df["product_type"]
        .value_counts()
        .to_string()
    )

    # --------------------------------------------------
    # 2. Check duplicate ASINs
    # --------------------------------------------------

    duplicate_asins = df[
        df["parent_asin"].duplicated()
    ]

    print(
        f"\nDuplicate parent_asins: "
        f"{len(duplicate_asins):,}"
    )

    # --------------------------------------------------
    # 3. Check missing values
    # --------------------------------------------------

    print("\nMissing values:")

    missing_values = df.isnull().sum()

    print(
        missing_values[
            missing_values > 0
        ].to_string()
    )

    # --------------------------------------------------
    # 4. Check rating threshold
    # --------------------------------------------------

    below_threshold = df[
        df["rating_number"] < 20
    ]

    print(
        f"\nProducts below rating threshold: "
        f"{len(below_threshold):,}"
    )

    # --------------------------------------------------
    # 5. Check required fields
    # --------------------------------------------------

    missing_asin = df["parent_asin"].isnull().sum()
    missing_title = df["title"].isnull().sum()

    print(
        f"\nMissing parent_asin: {missing_asin:,}"
    )

    print(
        f"Missing title: {missing_title:,}"
    )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    expected_counts = {
        "laptop": 4000,
        "tablet": 2500,
        "headphones": 4000,
    }

    actual_counts = (
        df["product_type"]
        .value_counts()
        .to_dict()
    )

    validation_passed = True

    if len(df) != 10500:
        validation_passed = False

    if df["parent_asin"].duplicated().any():
        validation_passed = False

    if len(below_threshold) > 0:
        validation_passed = False

    if missing_asin > 0:
        validation_passed = False

    if missing_title > 0:
        validation_passed = False

    for product_type, expected in expected_counts.items():

        if actual_counts.get(product_type, 0) != expected:
            validation_passed = False

    print("\n========================================")

    if validation_passed:
        print("VALIDATION PASSED")
    else:
        print("VALIDATION FAILED")

    print("========================================")


if __name__ == "__main__":
    validate_dataset()