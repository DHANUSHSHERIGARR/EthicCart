from pathlib import Path

import requests
from tqdm import tqdm


METADATA_URL = (
    "https://mcauleylab.ucsd.edu/public_datasets/"
    "data/amazon_2023/raw/meta_categories/"
    "meta_Electronics.jsonl.gz"
)

RAW_DATA_DIR = Path("data/raw")
METADATA_FILE = RAW_DATA_DIR / "meta_Electronics.jsonl.gz"

def download_file(url: str, output_path: Path) -> None:
    """Download a large file and resume if a previous download was interrupted."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    existing_size = output_path.stat().st_size if output_path.exists() else 0

    headers = {}

    if existing_size > 0:
        headers["Range"] = f"bytes={existing_size}-"
        print(f"Partial file found: {existing_size / (1024**2):.2f} MB")
        print("Attempting to resume download...")

    with requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=60,
    ) as response:

        response.raise_for_status()

        # 206 means the server accepted our Range request.
        if existing_size > 0 and response.status_code == 206:
            mode = "ab"
            total_size = existing_size + int(
                response.headers.get("content-length", 0)
            )
        else:
            # Server did not resume; start again safely.
            mode = "wb"
            existing_size = 0
            total_size = int(response.headers.get("content-length", 0))

        chunk_size = 1024 * 1024

        with open(output_path, mode) as file:
            with tqdm(
                total=total_size,
                initial=existing_size,
                unit="B",
                unit_scale=True,
                desc=output_path.name,
            ) as progress:

                for chunk in response.iter_content(
                    chunk_size=chunk_size
                ):
                    if chunk:
                        file.write(chunk)
                        progress.update(len(chunk))

def main():
    print("Starting EthicCart metadata download...")


    download_file(METADATA_URL, METADATA_FILE)

    print(f"Download complete: {METADATA_FILE}")


if __name__ == "__main__":
    main()