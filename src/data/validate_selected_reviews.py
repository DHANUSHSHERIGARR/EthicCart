import json
from collections import Counter
from pathlib import Path

import pandas as pd


PRODUCT_FILE = Path(
    "data/processed/selected_products.csv"
)

REVIEW_FILE = Path(
    "data/processed/selected_reviews.jsonl"
)


def validate_reviews():

    print("========================================")
    print("EthicCart Selected Review Validation")
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

    reviews_by_product = Counter()

    rating_counts = Counter()

    verified_counts = Counter()

    missing_text = 0

    missing_title = 0

    missing_parent_asin = 0

    duplicate_keys = set()

    duplicate_count = 0

    invalid_parent_asins = 0

    # --------------------------------------------------
    # Read reviews
    # --------------------------------------------------

    print("\nScanning extracted reviews...")

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

            # ------------------------------------------
            # Parent ASIN check
            # ------------------------------------------

            if not parent_asin:

                missing_parent_asin += 1

            else:

                reviews_by_product[
                    parent_asin
                ] += 1

                if parent_asin not in selected_asins:

                    invalid_parent_asins += 1

            # ------------------------------------------
            # Rating
            # ------------------------------------------

            rating = review.get("rating")

            if rating is not None:

                rating_counts[rating] += 1

            # ------------------------------------------
            # Review text
            # ------------------------------------------

            text = review.get("text")

            if (
                text is None
                or not str(text).strip()
            ):

                missing_text += 1

            # ------------------------------------------
            # Review title
            # ------------------------------------------

            title = review.get("title")

            if (
                title is None
                or not str(title).strip()
            ):

                missing_title += 1

            # ------------------------------------------
            # Verified purchase
            # ------------------------------------------

            verified = review.get(
                "verified_purchase"
            )

            verified_counts[
                str(verified)
            ] += 1

            # ------------------------------------------
            # Duplicate detection
            #
            # We use product + user + timestamp +
            # review text as a practical review key.
            # ------------------------------------------

            duplicate_key = (
                parent_asin,
                review.get("user_id"),
                review.get("timestamp"),
                review.get("text")
            )

            if duplicate_key in duplicate_keys:

                duplicate_count += 1

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

    print("\n========== REVIEW STATISTICS ==========")

    print(
        f"Total extracted reviews: "
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
    # Rating distribution
    # --------------------------------------------------

    print("\n========== RATING DISTRIBUTION ==========")

    for rating in sorted(rating_counts):

        print(
            f"{rating} stars: "
            f"{rating_counts[rating]:,}"
        )

    # --------------------------------------------------
    # Verified purchase distribution
    # --------------------------------------------------

    print(
        "\n========== VERIFIED PURCHASE =========="
    )

    for value, count in verified_counts.items():

        print(
            f"{value}: {count:,}"
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
        f"Missing review title: "
        f"{missing_title:,}"
    )

    print(
        f"Reviews linked to unselected products: "
        f"{invalid_parent_asins:,}"
    )

    print(
        f"Duplicate review records: "
        f"{duplicate_count:,}"
    )

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    validation_passed = True

    if total_reviews != 720975:

        validation_passed = False

    if missing_parent_asin > 0:

        validation_passed = False

    if invalid_parent_asins > 0:

        validation_passed = False

    print(
        "\n========================================"
    )

    if validation_passed:

        print(
            "REVIEW DATA VALIDATION PASSED"
        )

    else:

        print(
            "REVIEW DATA VALIDATION REQUIRES REVIEW"
        )

    print(
        "========================================"
    )


if __name__ == "__main__":

    validate_reviews()