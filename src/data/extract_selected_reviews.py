import gzip
import json
from pathlib import Path

import pandas as pd


PRODUCT_FILE = Path(
    "data/processed/selected_products.csv"
)

REVIEW_FILE = Path(
    "data/raw/Electronics.jsonl.gz"
)

OUTPUT_FILE = Path(
    "data/processed/selected_reviews.jsonl"
)


def load_selected_products():
    """Load the selected product parent ASINs."""

    df = pd.read_csv(PRODUCT_FILE)

    selected_asins = set(
        df["parent_asin"]
        .dropna()
        .astype(str)
    )

    print(
        f"Selected products loaded: "
        f"{len(selected_asins):,}"
    )

    return selected_asins


def extract_reviews(selected_asins):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    reviews_found = 0
    reviews_scanned = 0

    print(
        "\nScanning Electronics reviews..."
    )

    with gzip.open(
        REVIEW_FILE,
        "rt",
        encoding="utf-8"
    ) as review_file:

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as output_file:

            for line in review_file:

                reviews_scanned += 1

                review = json.loads(line)

                parent_asin = review.get(
                    "parent_asin"
                )

                if (
                    parent_asin
                    not in selected_asins
                ):
                    continue

                selected_review = {
                    "parent_asin": parent_asin,
                    "asin": review.get("asin"),
                    "rating": review.get("rating"),
                    "title": review.get("title"),
                    "text": review.get("text"),
                    "verified_purchase": review.get(
                        "verified_purchase"
                    ),
                    "helpful_vote": review.get(
                        "helpful_vote"
                    ),
                    "timestamp": review.get(
                        "timestamp"
                    ),
                    "user_id": review.get(
                        "user_id"
                    ),
                }

                output_file.write(
                    json.dumps(
                        selected_review,
                        ensure_ascii=False
                    )
                    + "\n"
                )

                reviews_found += 1

                if reviews_found % 10000 == 0:

                    print(
                        f"Reviews matched: "
                        f"{reviews_found:,} | "
                        f"Reviews scanned: "
                        f"{reviews_scanned:,}"
                    )

    print(
        "\n========== EXTRACTION COMPLETE =========="
    )

    print(
        f"Reviews scanned: "
        f"{reviews_scanned:,}"
    )

    print(
        f"Matching reviews: "
        f"{reviews_found:,}"
    )

    print(
        f"Output file: "
        f"{OUTPUT_FILE}"
    )


def main():

    print(
        "========================================"
    )

    print(
        "EthicCart Review Extraction"
    )

    print(
        "========================================"
    )

    selected_asins = load_selected_products()

    extract_reviews(selected_asins)


if __name__ == "__main__":
    main()