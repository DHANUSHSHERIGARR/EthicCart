import gzip
import json
from pathlib import Path


REVIEW_FILE = Path(
    "data/raw/Electronics.jsonl.gz"
)


def inspect_reviews(sample_size=5):

    print("========================================")
    print("EthicCart Review Dataset Inspection")
    print("========================================")

    with gzip.open(
        REVIEW_FILE,
        "rt",
        encoding="utf-8"
    ) as file:

        for index in range(sample_size):

            line = file.readline()

            if not line:
                break

            review = json.loads(line)

            print(
                f"\n========== REVIEW {index + 1} =========="
            )

            print("Fields:")
            print(list(review.keys()))

            print("\nReview record:")

            print(
                json.dumps(
                    review,
                    indent=2,
                    ensure_ascii=False
                )
            )


if __name__ == "__main__":
    inspect_reviews()