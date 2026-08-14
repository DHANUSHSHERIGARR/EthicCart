import json
from collections import Counter
from pathlib import Path

import pandas as pd


PRODUCT_FILE = Path(
    "data/processed/selected_products.csv"
)

REVIEW_FILE = Path(
    "data/processed/cleaned_reviews.jsonl"
)


def validate_cleaned_reviews():

    print("========================================")
    print("EthicCart Cleaned Review Validation")
    print("========================================")

    # --------------------------------------------------
    # Load selected products
    # --------------------------------------------------

    products = pd.read_csv(PRODUCT_FILE)

    selected_asins = set(
        products["parent_asin"]
        .dropna()
        .astype(str)
    )

    print(
        f"\nSelected products: "
        f"{len(selected_asins):,}"
    )

    # --------------------------------------------------
    # Counters
    # --------------------------------------------------

    total_reviews = 0
    missing_text = 0
    missing_parent_asin = 0
    unselected_products = 0

    rating_counts = Counter()
    reviews_by_product = Counter()

    duplicate_keys = set()
    duplicates = 0

    # --------------------------------------------------
    # Scan cleaned reviews
    # --------------------------------------------------

    print("\nScanning cleaned reviews...")

    with open(
        REVIEW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            review = json.loads(line)

            total_reviews += 1

            parent_asin = review.get(
                "parent_asin"
            )

            # Parent ASIN validation
            if not parent_asin:

                missing_parent_asin += 1

            else:

                reviews_by_product[
                    parent_asin
                ] += 1

                if parent_asin not in selected_asins:

                    unselected_products += 1

            # Review text validation
            text = review.get("text")

            if (
                text is None
                or not str(text).strip()
            ):

                missing_text += 1

            # Rating distribution
            rating = review.get("rating")

            if rating is not None:

                rating_counts[rating] += 1

            # Duplicate validation
            duplicate_key = (
                parent_asin,
                review.get("user_id"),
                review.get("timestamp"),
                text
            )

            if duplicate_key in duplicate_keys:

                duplicates += 1

            else:

                duplicate_keys.add(
                    duplicate_key
                )

    # --------------------------------------------------
    # Product coverage
    # --------------------------------------------------

    products_with_reviews = len(
        reviews_by_product
    )

    products_without_reviews = (
        len(selected_asins)
        - products_with_reviews
    )

    review_counts = list(
        reviews_by_product.values()
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print(
        "\n========== CLEANED DATASET =========="
    )

    print(
        f"Total cleaned reviews: "
        f"{total_reviews:,}"
    )

    print(
        f"Products with reviews: "
        f"{products_with_reviews:,}"
    )

    print(
        f"Products without reviews: "
        f"{products_without_reviews:,}"
    )

    if review_counts:

        print(
            f"Minimum reviews/product: "
            f"{min(review_counts):,}"
        )

        print(
            f"Maximum reviews/product: "
            f"{max(review_counts):,}"
        )

        print(
            f"Average reviews/product: "
            f"{sum(review_counts) / len(review_counts):.2f}"
        )

    # --------------------------------------------------
    # Data quality
    # --------------------------------------------------

    print(
        "\n========== DATA QUALITY =========="
    )

    print(
        f"Missing parent_asin: "
        f"{missing_parent_asin:,}"
    )

    print(
        f"Missing review text: "
        f"{missing_text:,}"
    )

    print(
        f"Reviews linked to unselected products: "
        f"{unselected_products:,}"
    )

    print(
        f"Duplicate review records: "
        f"{duplicates:,}"
    )

    # --------------------------------------------------
    # Rating distribution
    # --------------------------------------------------

    print(
        "\n========== RATING DISTRIBUTION =========="
    )

    for rating in sorted(rating_counts):

        print(
            f"{rating} stars: "
            f"{rating_counts[rating]:,}"
        )

    # --------------------------------------------------
    # Final status
    # --------------------------------------------------

    if (
        total_reviews > 0
        and missing_parent_asin == 0
        and missing_text == 0
        and unselected_products == 0
        and duplicates == 0
    ):

        print(
            "\nCLEANED REVIEW DATASET VALIDATION PASSED"
        )

    else:

        print(
            "\nCLEANED REVIEW DATASET REQUIRES REVIEW"
        )


if __name__ == "__main__":

    validate_cleaned_reviews()