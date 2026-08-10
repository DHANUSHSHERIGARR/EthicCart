import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path


METADATA_FILE = Path("data/raw/meta_Electronics.jsonl.gz")


TARGET_CATEGORIES = {
    "laptop": {
        "Laptops",
        "Traditional Laptops",
        "2 in 1 Laptops",
        "Gaming Laptops",
        "Touchscreen Laptops",
    },
    "tablet": {
        "Tablets",
        "Tablet PCs",
        "Fire Tablets",
        "Intel-Powered Tablets",
    },
    "headphones": {
        "Headphones & Earbuds",
        "Earbud Headphones",
        "Over-Ear Headphones",
        "On-Ear Headphones",
        "Open-Ear Headphones",
        "Headphones",
    },
}


def get_product_category(categories):
    """
    Determine whether a product belongs to one of our
    selected product domains.
    """

    categories = set(categories or [])

    matches = []

    for product_type, valid_categories in TARGET_CATEGORIES.items():

        if categories.intersection(valid_categories):
            matches.append(product_type)

    if not matches:
        return None

    # A product may appear in more than one category.
    # We keep the first match for now.
    return matches[0]


def analyze_review_availability():
    total_products = 0
    eligible_products = Counter()

    review_thresholds = {
        1: Counter(),
        5: Counter(),
        10: Counter(),
        20: Counter(),
        50: Counter(),
        100: Counter(),
    }

    rating_distributions = defaultdict(list)

    print("Analyzing review availability...")
    print("Scanning Electronics metadata...")

    with gzip.open(
        METADATA_FILE,
        "rt",
        encoding="utf-8"
    ) as file:

        for line in file:

            total_products += 1

            record = json.loads(line)

            categories = record.get("categories") or []

            product_type = get_product_category(categories)

            if product_type is None:
                continue

            rating_number = record.get("rating_number") or 0

            eligible_products[product_type] += 1

            rating_distributions[product_type].append(
                rating_number
            )

            for threshold in review_thresholds:

                if rating_number >= threshold:
                    review_thresholds[threshold][product_type] += 1

    print("\n========== REVIEW AVAILABILITY ==========")

    print(f"Total products scanned: {total_products:,}")

    print("\nEligible products:")

    for product_type, count in eligible_products.items():
        print(
            f"{product_type.title():<15}: {count:,}"
        )

    print("\nProducts meeting review-count thresholds:")

    print(
        f"{'Threshold':<12}"
        f"{'Laptops':>12}"
        f"{'Tablets':>12}"
        f"{'Headphones':>15}"
    )

    print("-" * 51)

    for threshold in review_thresholds:

        print(
            f"{threshold:<12}"
            f"{review_thresholds[threshold]['laptop']:>12,}"
            f"{review_thresholds[threshold]['tablet']:>12,}"
            f"{review_thresholds[threshold]['headphones']:>15,}"
        )


if __name__ == "__main__":
    analyze_review_availability()