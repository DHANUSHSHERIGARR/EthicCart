# EthicCart --- Data Acquisition & Selection

## 1. Overview

This document records the complete Phase 1C data acquisition,
investigation, selection, extraction, cleaning, and validation workflow
used for EthicCart.

The objective is to create a reproducible and validated product-review
dataset for later NLP, ethical evidence extraction, machine-learning,
and explainability work.

The original source data is preserved separately from project-generated
data.

------------------------------------------------------------------------

## 2. Dataset Source

EthicCart uses the **Amazon Reviews'23** dataset provided by the McAuley
Lab at the University of California, San Diego.

The project initially focused on the **Electronics** category.

Two raw datasets were acquired:

1.  Product metadata
2.  Customer reviews

Raw datasets are stored under:

`data/raw/`

The raw datasets are not modified during processing.

------------------------------------------------------------------------

## 3. Raw Product Metadata

The Electronics metadata contains **1,610,012 products**.

Important metadata fields include:

-   `main_category`
-   `title`
-   `average_rating`
-   `rating_number`
-   `features`
-   `description`
-   `price`
-   `images`
-   `videos`
-   `store`
-   `categories`
-   `details`
-   `parent_asin`
-   `bought_together`

The `parent_asin` field is used as the primary product identifier for
connecting product metadata with customer reviews.

Raw metadata file:

`data/raw/meta_Electronics.jsonl.gz`

------------------------------------------------------------------------

## 4. Metadata Inspection

The metadata was inspected directly before product selection.

The inspection confirmed that product records contain structured and
textual information such as:

-   Product title
-   Average rating
-   Number of ratings
-   Product features
-   Product description
-   Price
-   Store
-   Product categories
-   Product details
-   Parent ASIN

This step was performed so that product selection would be based on the
actual dataset structure rather than assumed category names.

Script:

`src/data/inspect_metadata.py`

------------------------------------------------------------------------

## 5. Category Investigation

The complete Electronics metadata was scanned to understand the actual
category taxonomy.

The project did not assume that categories such as smartphones, laptops,
or tablets were represented cleanly.

The actual category labels and frequencies were investigated.

Three sufficiently useful product domains were selected:

1.  Laptops
2.  Tablets
3.  Headphones/Earbuds

Script:

`src/data/analyze_categories.py`

------------------------------------------------------------------------

## 6. Smartphone Investigation

Smartphones were initially considered as a target category.

However, the Electronics metadata did not provide a sufficiently large
and clean smartphone population.

Many phone-related matches represented accessories rather than actual
smartphones.

Examples observed included:

-   `Cell Phone Headsets`
-   `Mobile Broadband Devices`
-   `Android Accessories`
-   `Cell Phones & Accessories`
-   `iPhone Cases`
-   `Renewed Phones`

Because the clean smartphone representation was insufficient for the
intended analysis, smartphones were excluded from the final selection.

Script:

`src/data/find_smartphone_candidates.py`

This decision was based on the actual category distribution observed in
the dataset.

------------------------------------------------------------------------

## 7. Selected Product Domains

The final product domains were:

1.  Laptops
2.  Tablets
3.  Headphones/Earbuds

These domains provide sufficiently large candidate populations while
keeping the project computationally manageable.

------------------------------------------------------------------------

## 8. Laptop Category Selection

The following labels were used:

-   `Laptops`
-   `Traditional Laptops`
-   `2 in 1 Laptops`
-   `Gaming Laptops`
-   `Touchscreen Laptops`

Broad accessory categories were not directly treated as laptop products,
for example:

-   `Laptop Accessories`
-   `Laptop Replacement Parts`
-   `Laptop Backpacks & Bags`
-   `Laptop Travel Accessories`

------------------------------------------------------------------------

## 9. Tablet Category Selection

The following labels were used:

-   `Tablets`
-   `Tablet PCs`
-   `Fire Tablets`
-   `Intel-Powered Tablets`

Broad tablet-accessory categories were not directly treated as tablet
products.

------------------------------------------------------------------------

## 10. Headphones/Earbuds Category Selection

The following labels were used:

-   `Headphones & Earbuds`
-   `Earbud Headphones`
-   `Over-Ear Headphones`
-   `On-Ear Headphones`
-   `Open-Ear Headphones`
-   `Headphones`

Broad accessory categories were not directly selected as the main
headphone product category.

------------------------------------------------------------------------

## 11. Review Availability Analysis

The metadata field `rating_number` was used as an initial indicator of
review activity.

Multiple thresholds were analyzed to understand the available candidate
population.

The final candidate criterion was:

`rating_number >= 20`

Products with fewer than 20 ratings were excluded from the candidate
pool.

Script:

`src/data/analyze_review_availability.py`

------------------------------------------------------------------------

## 12. Reason for the 20-Rating Threshold

The threshold of 20 ratings was selected as a balance between:

-   Having sufficient customer feedback for NLP analysis
-   Maintaining a sufficiently large candidate pool
-   Keeping the project computationally manageable

The threshold is only a **data-selection criterion**.

It is not an ethical label.

Having at least 20 ratings does not mean that a product is ethical or
unethical.

Actual review records were later extracted and validated against the
selected products.

------------------------------------------------------------------------

## 13. Final Product Selection

After category filtering and review-activity filtering, a reproducible
random selection was performed using a fixed random seed.

Final target:

  Product Type             Selected
  -------------------- ------------
  Laptops                     4,000
  Tablets                     2,500
  Headphones/Earbuds          4,000
  **Total**              **10,500**

Script:

`src/data/select_products.py`

Output:

`data/processed/selected_products.csv`

------------------------------------------------------------------------

## 14. Product Dataset Validation

The selected product dataset was validated for:

-   Total number of records
-   Product-type distribution
-   Duplicate `parent_asin`
-   Missing `parent_asin`
-   Missing product titles
-   Products below the minimum rating threshold

Validation results:

  Check                         Result
  --------------------------- --------
  Total products                10,500
  Laptops                        4,000
  Tablets                        2,500
  Headphones                     4,000
  Duplicate `parent_asin`            0
  Missing `parent_asin`              0
  Missing title                      0
  Products below 20 ratings          0

Missing price values were retained as missing. They were not
artificially assigned and will be handled later if price is required
during preprocessing.

Script:

`src/data/validate_selected_products.py`

------------------------------------------------------------------------

## 15. Customer Review Dataset

The Electronics customer-review dataset was downloaded as a compressed
JSONL file.

Raw review file:

`data/raw/Electronics.jsonl.gz`

The download script supports large-file downloads and was updated to
resume an interrupted download when possible.

Script:

`src/data/download_data.py`

------------------------------------------------------------------------

## 16. Review Schema Inspection

The review dataset was inspected before extraction.

Observed fields:

-   `rating`
-   `title`
-   `text`
-   `images`
-   `asin`
-   `parent_asin`
-   `user_id`
-   `timestamp`
-   `helpful_vote`
-   `verified_purchase`

Important fields:

### `parent_asin`

Connects a review with a selected product.

### `asin`

Identifies the specific product or variant associated with the review.

### `rating`

Contains the customer's rating.

### `title`

Contains the review title.

### `text`

Contains the main customer-written review and is an important input for
later NLP processing.

### `verified_purchase`

Indicates whether the review is associated with a verified purchase.

### `helpful_vote`

Contains the number of helpful votes.

### `timestamp`

Contains the review timestamp.

### `user_id`

Identifies the reviewer and is useful for duplicate-review analysis.

Script:

`src/data/inspect_reviews.py`

------------------------------------------------------------------------

## 17. Review Matching Strategy

The selected product dataset uses `parent_asin` as its primary product
identifier.

Reviews were therefore matched using:

`review.parent_asin == selected_product.parent_asin`

The extraction process loaded the 10,500 selected `parent_asin` values
into a lookup set.

The complete Electronics review dataset was then scanned as a stream.

Conceptually:

**Selected products → 10,500 parent ASINs → lookup set → scan reviews →
compare `parent_asin` → keep matching reviews**

Streaming was used so the complete approximately 44-million-review file
did not have to be loaded into memory at once.

Script:

`src/data/extract_selected_reviews.py`

------------------------------------------------------------------------

## 18. Review Extraction Results

The complete Electronics review file was scanned.

Results:

-   **Reviews scanned: 43,886,944**
-   **Matching reviews: 720,975**

Output:

`data/processed/selected_reviews.jsonl`

The extracted file was approximately **414 MB**.

It remains local and is not intended to be committed to GitHub.

------------------------------------------------------------------------

## 19. Initial Review Validation

The extracted review dataset was validated for:

-   Total extracted reviews
-   Products with reviews
-   Products without reviews
-   Missing `parent_asin`
-   Missing review text
-   Missing review title
-   Reviews linked to unselected products
-   Duplicate review records
-   Rating distribution
-   Verified-purchase distribution

Results:

  Metric                                     Result
  --------------------------------------- ---------
  Total extracted reviews                   720,975
  Products with reviews                      10,499
  Products without reviews                        1
  Missing `parent_asin`                           0
  Missing review text                           932
  Missing review title                            0
  Reviews linked to unselected products           0
  Duplicate review records                    8,459

Script:

`src/data/validate_selected_reviews.py`

------------------------------------------------------------------------

## 20. Initial Rating Distribution

The extracted reviews contained:

  Rating      Reviews
  --------- ---------
  1 star      116,732
  2 stars      53,827
  3 stars      60,808
  4 stars     104,714
  5 stars     384,894

Ratings are customer-feedback signals, not direct ethical labels.

A five-star review does not automatically mean that a product is
ethical, and a one-star review does not automatically mean that a
product is unethical.

Later ethical analysis will require evidence related to defined ethical
dimensions.

------------------------------------------------------------------------

## 21. Verified Purchase Distribution

The extracted review dataset contained:

  Verified Purchase     Reviews
  ------------------- ---------
  True                  645,022
  False                  75,953

`verified_purchase` is retained as a possible supporting signal for
later analysis and is not used as an ethical label.

------------------------------------------------------------------------

## 22. Duplicate Review Analysis

Initial validation identified:

**8,459 duplicate review records.**

Duplicate samples were investigated using review information including:

-   `parent_asin`
-   `user_id`
-   `timestamp`
-   `rating`
-   `title`
-   `text`

Repeated copies of the same review information were observed.

Keeping duplicate records could cause the same customer opinion to
receive excessive weight during downstream analysis.

Therefore, duplicate review records were removed during cleaning.

Script:

`src/data/analyze_review_duplicates.py`

------------------------------------------------------------------------

## 23. Review Cleaning

Two main cleaning operations were performed.

### 23.1 Remove missing review text

Reviews with missing review text were removed because the downstream NLP
pipeline requires usable textual evidence.

Removed:

**932 reviews**

### 23.2 Remove duplicate reviews

Duplicate review records were removed using the duplicate-detection
logic implemented in the cleaning script.

Removed:

**8,449 reviews**

The original extracted review dataset was retained separately.

Script:

`src/data/clean_reviews.py`

------------------------------------------------------------------------

## 24. Cleaning Results

The cleaning process produced:

  Metric                                 Count
  ------------------------------ -------------
  Original extracted reviews           720,975
  Duplicate reviews removed              8,449
  Missing-text reviews removed             932
  **Final cleaned reviews**        **711,594**

Output:

`data/processed/cleaned_reviews.jsonl`

The cleaned file was approximately **409 MB**.

It remains local and is not intended to be committed to GitHub.

------------------------------------------------------------------------

## 25. Final Cleaned Review Validation

The cleaned review dataset was independently validated.

Final results:

  Metric                        Result
  -------------------------- ---------
  Total cleaned reviews        711,594
  Products with reviews         10,498
  Products without reviews           2
  Minimum reviews/product            1
  Maximum reviews/product       11,365
  Average reviews/product        67.78

Data-quality results:

  Check                                     Result
  --------------------------------------- --------
  Missing `parent_asin`                          0
  Missing review text                            0
  Reviews linked to unselected products          0
  Duplicate review records                       0

**CLEANED REVIEW DATASET VALIDATION PASSED**

Script:

`src/data/validate_cleaned_reviews.py`

------------------------------------------------------------------------

## 26. Final Rating Distribution

After cleaning:

  Rating      Reviews
  --------- ---------
  1 star      115,125
  2 stars      53,140
  3 stars      60,048
  4 stars     103,476
  5 stars     379,805

The cleaned dataset contains both positive and negative customer
experiences and therefore provides a useful textual evidence base for
later NLP processing.

------------------------------------------------------------------------

## 27. Products Without Usable Review Evidence

The selected product dataset contains **10,500 products**.

After review extraction and cleaning, **10,498 products** have usable
review evidence.

Therefore, **2 products** do not have usable review evidence after
cleaning.

These products should not automatically be classified as ethical or
unethical.

A later stage can use an **Insufficient Evidence** state when there is
not enough evidence to make a reliable ethical assessment.

------------------------------------------------------------------------

## 28. Ethical Evidence Principle

EthicCart is intended to evaluate products using evidence rather than
arbitrary manually assigned ethical scores.

The system should not simply assign values such as:

-   Privacy = 8
-   Safety = 6
-   Transparency = 9

without supporting evidence.

The intended future workflow is:

**Product Metadata + Customer Reviews → NLP Processing → Ethical
Evidence Extraction → Ethical Dimensions → Evidence-Based Evaluation**

Potential ethical dimensions include:

-   Transparency
-   Safety
-   Privacy
-   Environmental impact
-   Sustainability

The exact operational definitions and labeling strategy will be
established during later project stages.

------------------------------------------------------------------------

## 29. Raw and Processed Data Separation

A strict separation is maintained between source data and
project-generated data.

### Raw data

Stored under:

`data/raw/`

Current raw files:

-   `data/raw/meta_Electronics.jsonl.gz`
-   `data/raw/Electronics.jsonl.gz`

The raw files are not modified during processing.

### Processed data

Stored under:

`data/processed/`

Current generated datasets:

-   `data/processed/selected_products.csv`
-   `data/processed/selected_reviews.jsonl`
-   `data/processed/cleaned_reviews.jsonl`

------------------------------------------------------------------------

## 30. Git and Large-File Policy

The complete Amazon datasets and generated review files are too large
for normal Git repository storage.

The `.gitignore` excludes:

-   `data/raw/`
-   `data/processed/`

The repository should contain the processing scripts, documentation, and
other reproducibility files rather than the full multi-gigabyte
datasets.

Large datasets remain local.

------------------------------------------------------------------------

## 31. Reproducibility

The workflow is implemented through Python scripts under:

`src/data/`

Scripts created and used during this stage:

-   `download_data.py`
-   `inspect_metadata.py`
-   `analyze_categories.py`
-   `find_smartphone_candidates.py`
-   `analyze_review_availability.py`
-   `select_products.py`
-   `validate_selected_products.py`
-   `inspect_reviews.py`
-   `extract_selected_reviews.py`
-   `validate_selected_reviews.py`
-   `analyze_review_duplicates.py`
-   `clean_reviews.py`
-   `validate_cleaned_reviews.py`

The product-selection process uses a fixed random seed so the selected
product set can be reproduced.

------------------------------------------------------------------------

## 32. Complete Phase 1C Pipeline

The complete workflow is:

**Amazon Reviews'23**

→ Electronics metadata

→ Metadata inspection

→ Category investigation

→ Smartphone investigation

→ Select Laptops / Tablets / Headphones

→ Review-activity filtering (`rating_number >= 20`)

→ Reproducible product selection

→ **10,500 selected products**

→ Product validation

→ Download Electronics reviews

→ Review schema inspection

→ Scan **43,886,944 reviews**

→ Match reviews using `parent_asin`

→ **720,975 matching reviews**

→ Review validation

→ Duplicate investigation

→ Remove **8,449 duplicate records**

→ Remove **932 missing-text records**

→ **711,594 cleaned reviews**

→ Final validation

→ Cleaned dataset ready for downstream NLP

------------------------------------------------------------------------

## 33. Current Dataset Summary

  Dataset Component                        Result
  --------------------------------- -------------
  Electronics products scanned          1,610,012
  Selected products                        10,500
  Laptops                                   4,000
  Tablets                                   2,500
  Headphones/Earbuds                        4,000
  Reviews scanned                      43,886,944
  Matching reviews                        720,975
  Duplicate reviews removed                 8,449
  Missing-text reviews removed                932
  **Final cleaned reviews**           **711,594**
  Products with usable reviews             10,498
  Products without usable reviews               2

------------------------------------------------------------------------

## 34. Files Created During This Stage

### Documentation

`docs/data-acquisition.md`

### Product acquisition and selection

-   `src/data/download_data.py`
-   `src/data/inspect_metadata.py`
-   `src/data/analyze_categories.py`
-   `src/data/find_smartphone_candidates.py`
-   `src/data/analyze_review_availability.py`
-   `src/data/select_products.py`
-   `src/data/validate_selected_products.py`

### Review processing

-   `src/data/inspect_reviews.py`
-   `src/data/extract_selected_reviews.py`
-   `src/data/validate_selected_reviews.py`
-   `src/data/analyze_review_duplicates.py`
-   `src/data/clean_reviews.py`
-   `src/data/validate_cleaned_reviews.py`

### Generated datasets

-   `data/processed/selected_products.csv`
-   `data/processed/selected_reviews.jsonl`
-   `data/processed/cleaned_reviews.jsonl`

The large datasets remain local and are excluded from version control.

------------------------------------------------------------------------

## 35. Phase 1C Completion Status

Completed:

-   [x] Acquire Electronics metadata
-   [x] Inspect metadata schema
-   [x] Investigate Electronics categories
-   [x] Investigate smartphone representation
-   [x] Select target product domains
-   [x] Analyze review availability
-   [x] Select 10,500 products
-   [x] Validate selected products
-   [x] Acquire Electronics reviews
-   [x] Inspect review schema
-   [x] Extract reviews using `parent_asin`
-   [x] Validate extracted reviews
-   [x] Analyze duplicate reviews
-   [x] Clean duplicate reviews
-   [x] Remove missing-text reviews
-   [x] Validate cleaned reviews
-   [x] Document the complete data-acquisition process

------------------------------------------------------------------------

## 36. Phase 1C Outcome

EthicCart now has a validated dataset consisting of:

-   **10,500 selected products**
-   **711,594 cleaned customer reviews**

The product dataset covers:

-   Laptops
-   Tablets
-   Headphones/Earbuds

The review dataset contains cleaned customer feedback linked to the
selected products through `parent_asin`.

The cleaned dataset is ready for the next stage:

**Data Preprocessing → NLP / Ethical Evidence Extraction**
