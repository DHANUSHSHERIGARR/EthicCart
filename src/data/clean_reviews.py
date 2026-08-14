import json
from pathlib import Path


INPUT_FILE = Path(
    "data/processed/selected_reviews.jsonl"
)

OUTPUT_FILE = Path(
    "data/processed/cleaned_reviews.jsonl"
)


def clean_reviews():

    print("========================================")
    print("EthicCart Review Cleaning")
    print("========================================")

    total_reviews = 0
    duplicate_reviews = 0
    missing_text_reviews = 0
    cleaned_reviews = 0

    seen = set()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as input_file:

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as output_file:

            for line in input_file:

                total_reviews += 1

                review = json.loads(line)

                # ----------------------------------------
                # Check review text
                # ----------------------------------------

                text = review.get("text")

                if (
                    text is None
                    or not str(text).strip()
                ):

                    missing_text_reviews += 1
                    continue

                # ----------------------------------------
                # Detect exact duplicate reviews
                # ----------------------------------------

                duplicate_key = (
                    review.get("parent_asin"),
                    review.get("user_id"),
                    review.get("timestamp"),
                    text
                )

                if duplicate_key in seen:

                    duplicate_reviews += 1
                    continue

                seen.add(duplicate_key)

                # ----------------------------------------
                # Keep cleaned review
                # ----------------------------------------

                cleaned_review = {
                    "parent_asin": review.get(
                        "parent_asin"
                    ),
                    "asin": review.get("asin"),
                    "rating": review.get("rating"),
                    "title": review.get("title"),
                    "text": str(text).strip(),
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
                        cleaned_review,
                        ensure_ascii=False
                    )
                    + "\n"
                )

                cleaned_reviews += 1

    print(
        "\n========== CLEANING COMPLETE =========="
    )

    print(
        f"Original reviews: "
        f"{total_reviews:,}"
    )

    print(
        f"Removed duplicates: "
        f"{duplicate_reviews:,}"
    )

    print(
        f"Removed missing-text reviews: "
        f"{missing_text_reviews:,}"
    )

    print(
        f"Final cleaned reviews: "
        f"{cleaned_reviews:,}"
    )

    print(
        f"\nOutput file: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    clean_reviews()