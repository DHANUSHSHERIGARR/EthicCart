import gzip
import json
from pathlib import Path


METADATA_FILE = Path("data/raw/meta_Electronics.jsonl.gz")


POSITIVE_KEYWORDS = [
    "smartphone",
    "cell phone",
    "cellphone",
    "iphone",
    "galaxy",
    "pixel",
    "oneplus",
    "motorola",
    "xiaomi",
]

ACCESSORY_KEYWORDS = [
    "case",
    "cover",
    "charger",
    "cable",
    "screen protector",
    "headset",
    "earbuds",
    "mount",
    "holder",
    "stand",
    "replacement",
]


def find_candidates(sample_limit: int = 50) -> None:
    candidates = []
    scanned = 0

    print("Searching product metadata for smartphone candidates...")

    with gzip.open(METADATA_FILE, "rt", encoding="utf-8") as file:

        for line in file:
            scanned += 1

            record = json.loads(line)

            title = record.get("title") or ""
            description = " ".join(record.get("description") or [])
            features = " ".join(record.get("features") or [])
            categories = " ".join(record.get("categories") or [])

            searchable_text = (
                f"{title} "
                f"{description} "
                f"{features} "
                f"{categories}"
            ).lower()

            has_positive_signal = any(
                keyword in searchable_text
                for keyword in POSITIVE_KEYWORDS
            )

            has_accessory_signal = any(
                keyword in searchable_text
                for keyword in ACCESSORY_KEYWORDS
            )

            if has_positive_signal and not has_accessory_signal:

                candidates.append(
                    {
                        "title": title,
                        "categories": record.get("categories"),
                        "store": record.get("store"),
                        "parent_asin": record.get("parent_asin"),
                    }
                )

                if len(candidates) >= sample_limit:
                    break

    print("\n========== SMARTPHONE CANDIDATES ==========")
    print(f"Products scanned: {scanned:,}")
    print(f"Candidates found: {len(candidates):,}")

    for index, product in enumerate(candidates, start=1):
        print(f"\n--- Candidate {index} ---")
        print(f"Title: {product['title']}")
        print(f"Categories: {product['categories']}")
        print(f"Store: {product['store']}")
        print(f"Parent ASIN: {product['parent_asin']}")


if __name__ == "__main__":
    find_candidates()