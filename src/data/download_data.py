from pathlib import Path

import requests
from tqdm import tqdm


# ============================================================
# DATASET URLs
# ============================================================

METADATA_URL = (
    "https://mcauleylab.ucsd.edu/public_datasets/"
    "data/amazon_2023/raw/meta_categories/"
    "meta_Electronics.jsonl.gz"
)

REVIEW_URL = (
    "https://mcauleylab.ucsd.edu/public_datasets/"
    "data/amazon_2023/raw/review_categories/"
    "Electronics.jsonl.gz"
)


# ============================================================
# LOCAL FILE LOCATIONS
# ============================================================

RAW_DATA_DIR = Path("data/raw")

METADATA_FILE = (
    RAW_DATA_DIR / "meta_Electronics.jsonl.gz"
)

REVIEW_FILE = (
    RAW_DATA_DIR / "Electronics.jsonl.gz"
)


# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def download_file(url: str, output_path: Path) -> None:
    """
    Download a large file.

    If a previous download was interrupted, attempt to
    continue from where it stopped.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Check whether a partial file already exists
    existing_size = (
        output_path.stat().st_size
        if output_path.exists()
        else 0
    )

    headers = {}

    # If a partial file exists, request the remaining bytes
    if existing_size > 0:
        headers["Range"] = (
            f"bytes={existing_size}-"
        )

        print(
            f"Partial file found: "
            f"{existing_size / (1024**2):.2f} MB"
        )

        print(
            "Attempting to resume download..."
        )

    # Start HTTP request
    with requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=60,
    ) as response:

        response.raise_for_status()

        # ----------------------------------------------------
        # Server accepted resume request
        # ----------------------------------------------------

        if (
            existing_size > 0
            and response.status_code == 206
        ):

            mode = "ab"

            total_size = (
                existing_size
                + int(
                    response.headers.get(
                        "content-length",
                        0
                    )
                )
            )

        # ----------------------------------------------------
        # Start download from beginning
        # ----------------------------------------------------

        else:

            mode = "wb"

            existing_size = 0

            total_size = int(
                response.headers.get(
                    "content-length",
                    0
                )
            )

        # Download in 1 MB chunks
        chunk_size = 1024 * 1024

        with open(
            output_path,
            mode
        ) as file:

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

                        progress.update(
                            len(chunk)
                        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print(
        "Starting EthicCart data acquisition..."
    )

    # --------------------------------------------------------
    # PRODUCT METADATA
    # --------------------------------------------------------

    print(
        "\nChecking product metadata..."
    )

    if METADATA_FILE.exists():

        print(
            f"Metadata already exists: "
            f"{METADATA_FILE}"
        )

        print(
            "Skipping metadata download."
        )

    else:

        print(
            "Metadata file not found."
        )

        print(
            "Downloading product metadata..."
        )

        download_file(
            METADATA_URL,
            METADATA_FILE
        )

        print(
            f"Metadata download complete: "
            f"{METADATA_FILE}"
        )

    # --------------------------------------------------------
    # CUSTOMER REVIEWS
    # --------------------------------------------------------

    print(
        "\nDownloading customer reviews..."
    )

    download_file(
        REVIEW_URL,
        REVIEW_FILE
    )

    print(
        f"\nReview download complete: "
        f"{REVIEW_FILE}"
    )

    print(
        "\nEthicCart data acquisition completed."
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()