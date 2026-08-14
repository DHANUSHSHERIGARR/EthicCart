import json
from pathlib import Path


REVIEW_FILE = Path(
    "data/processed/selected_reviews.jsonl"
)


def analyze_duplicates(sample_limit=10):

    print("========================================")
    print("EthicCart Duplicate Review Analysis")
    print("========================================")

    seen = set()
    duplicates = []

    with open(
        REVIEW_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            review = json.loads(line)

            key = (
                review.get("parent_asin"),
                review.get("user_id"),
                review.get("timestamp"),
                review.get("text")
            )

            if key in seen:

                if len(duplicates) < sample_limit:
                    duplicates.append(review)

            else:

                seen.add(key)

    print(
        f"\nDuplicate samples collected: "
        f"{len(duplicates)}"
    )

    for index, review in enumerate(
        duplicates,
        start=1
    ):

        print(
            f"\n========== DUPLICATE SAMPLE "
            f"{index} =========="
        )

        print(
            f"Parent ASIN: "
            f"{review.get('parent_asin')}"
        )

        print(
            f"User ID: "
            f"{review.get('user_id')}"
        )

        print(
            f"Timestamp: "
            f"{review.get('timestamp')}"
        )

        print(
            f"Rating: "
            f"{review.get('rating')}"
        )

        print(
            f"Title: "
            f"{review.get('title')}"
        )

        text = review.get("text") or ""

        print(
            f"Text: {text[:300]}"
        )


if __name__ == "__main__":
    analyze_duplicates()