import gzip
import json
from collections import Counter
from pathlib import Path


METADATA_FILE = Path("data/raw/meta_Electronics.jsonl.gz")

TARGET_KEYWORDS = {
    "headphone",
    "earbud",
}

def analyze_categories() -> None:
    category_counts = Counter()
    total_products = 0

    print("Analyzing Electronics category paths...")
    print("Please wait. The metadata file is large.")

    with gzip.open(METADATA_FILE, "rt", encoding="utf-8") as file:

        for line in file:
            total_products += 1

            record = json.loads(line)

            categories = record.get("categories") or []

            for category in categories:

                category_lower = category.lower()

                if any(
                    keyword in category_lower
                    for keyword in TARGET_KEYWORDS
                ):
                    category_counts[category] += 1

    print("\n========== CATEGORY ANALYSIS ==========")
    print(f"Total products scanned: {total_products:,}")

    print("\nMatching categories:")

    for category, count in category_counts.most_common():
        print(f"{category}: {count:,}")


if __name__ == "__main__":
    analyze_categories()