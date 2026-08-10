import gzip
import json
from pathlib import Path


METADATA_FILE = Path("data/raw/meta_Electronics.jsonl.gz")


def inspect_metadata(sample_size: int = 5) -> None:
    """Read and display a small sample from the metadata file."""

    with gzip.open(METADATA_FILE, "rt", encoding="utf-8") as file:

        for index, line in enumerate(file):

            record = json.loads(line)

            print(f"\n--- Product {index + 1} ---")
            print("Fields:")
            print(list(record.keys()))

            print("\nProduct record:")
            print(json.dumps(record, indent=2, ensure_ascii=False))

            if index + 1 >= sample_size:
                break


def main():
    print("Inspecting Amazon Electronics metadata...")
    inspect_metadata()


if __name__ == "__main__":
    main()