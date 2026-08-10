import gzip
import json
import random
from pathlib import Path

import pandas as pd


METADATA_FILE = Path("data/raw/meta_Electronics.jsonl.gz")
OUTPUT_FILE = Path("data/processed/selected_products.csv")

MIN_RATINGS = 20
RANDOM_STATE = 42

TARGET_COUNTS = {
    "laptop": 4000,
    "tablet": 2500,
    "headphones": 4000,
}


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


def determine_product_type(categories):
    """Return the product type based on the selected category rules."""

    categories = set(categories or [])

    matches = []

    for product_type, valid_categories in TARGET_CATEGORIES.items():

        if categories.intersection(valid_categories):
            matches.append(product_type)

    if not matches:
        return None

    # If a product matches multiple target domains,
    # we use the first matching domain.
    return matches[0]


def load_candidates():
    """Read metadata and collect eligible product candidates."""

    candidates = {
        "laptop": [],
        "tablet": [],
        "headphones": [],
    }

    seen_asins = set()

    total_scanned = 0

    print("Scanning metadata for eligible products...")

    with gzip.open(
        METADATA_FILE,
        "rt",
        encoding="utf-8"
    ) as file:

        for line in file:

            total_scanned += 1

            record = json.loads(line)

            parent_asin = record.get("parent_asin")

            if not parent_asin:
                continue

            if parent_asin in seen_asins:
                continue

            rating_number = record.get("rating_number") or 0

            if rating_number < MIN_RATINGS:
                continue

            title = record.get("title")

            if not title:
                continue

            product_type = determine_product_type(
                record.get("categories")
            )

            if product_type is None:
                continue

            seen_asins.add(parent_asin)

            candidates[product_type].append(
                {
                    "parent_asin": parent_asin,
                    "product_type": product_type,
                    "title": title,
                    "average_rating": record.get(
                        "average_rating"
                    ),
                    "rating_number": rating_number,
                    "price": record.get("price"),
                    "store": record.get("store"),
                    "categories": json.dumps(
                        record.get("categories"),
                        ensure_ascii=False,
                    ),
                    "features": json.dumps(
                        record.get("features"),
                        ensure_ascii=False,
                    ),
                    "description": json.dumps(
                        record.get("description"),
                        ensure_ascii=False,
                    ),
                }
            )

    print(f"Total products scanned: {total_scanned:,}")

    return candidates


def select_products(candidates):
    """Randomly select the required number of products."""

    random.seed(RANDOM_STATE)

    selected = []

    for product_type, target_count in TARGET_COUNTS.items():

        available = candidates[product_type]

        if len(available) < target_count:
            raise ValueError(
                f"Not enough {product_type} products. "
                f"Needed {target_count}, "
                f"found {len(available)}."
            )

        selected_products = random.sample(
            available,
            target_count,
        )

        selected.extend(selected_products)

        print(
            f"{product_type.title():<15}: "
            f"{len(selected_products):,} selected "
            f"from {len(available):,} candidates"
        )

    return selected


def save_products(products):
    """Save selected products to the processed dataset."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(products)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print(f"\nSaved dataset: {OUTPUT_FILE}")
    print(f"Total selected products: {len(df):,}")


def main():

    print("========================================")
    print("EthicCart Product Selection")
    print("========================================")

    candidates = load_candidates()

    selected_products = select_products(
        candidates
    )

    save_products(selected_products)


if __name__ == "__main__":
    main()