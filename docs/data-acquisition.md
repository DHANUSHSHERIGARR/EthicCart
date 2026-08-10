# EthicCart — Data Acquisition & Selection

## 1. Dataset Source

EthicCart uses the Amazon Reviews'23 dataset provided by the McAuley Lab at UC San Diego.

The project initially investigates the Electronics category of the dataset.

The raw metadata contains approximately 1.61 million Electronics products.

---

## 2. Raw Product Metadata

The metadata provides information including:

- Product title
- Average rating
- Rating count
- Features
- Description
- Price
- Store
- Product categories
- Product details
- Parent ASIN

The `parent_asin` field is used as the primary product identifier for connecting product metadata with customer reviews.

---

## 3. Category Investigation

The Electronics metadata was scanned to understand the actual category taxonomy rather than assuming that product categories would follow expected names.

Three product domains were selected:

1. Laptops
2. Tablets
3. Headphones/Earbuds

Smartphones were investigated but were not selected because the Electronics metadata contained insufficient clean smartphone category representation. Many phone-related results represented accessories rather than actual smartphones.

---

## 4. Selected Product Categories

### Laptops

The following category labels were used:

- Laptops
- Traditional Laptops
- 2 in 1 Laptops
- Gaming Laptops
- Touchscreen Laptops

### Tablets

The following category labels were used:

- Tablets
- Tablet PCs
- Fire Tablets
- Intel-Powered Tablets

### Headphones/Earbuds

The following category labels were used:

- Headphones & Earbuds
- Earbud Headphones
- Over-Ear Headphones
- On-Ear Headphones
- Open-Ear Headphones
- Headphones

Broad accessory categories were not directly selected as product categories.

---

## 5. Review Availability Criterion

The metadata field `rating_number` was used as an initial indicator of product review activity.

Products with fewer than 20 ratings were excluded from the candidate pool.

The threshold of 20 was selected as a balance between:

- Having sufficient customer feedback for NLP analysis
- Maintaining a sufficiently large product pool
- Keeping the project computationally manageable

This value represents rating activity in the metadata and will be validated against the actual review records later.

---

## 6. Final Product Selection

From the eligible candidate pool, a reproducible random selection was performed using a fixed random seed.

Final target:

| Product Type | Selected |
|--------------|----------|
| Laptops | 4,000 |
| Tablets | 2,500 |
| Headphones/Earbuds | 4,000 |
| **Total** | **10,500** |

The selected products are stored in:

`data/processed/selected_products.csv`

---

## 7. Validation

The selected dataset was validated for:

- Total number of records
- Product-type distribution
- Duplicate `parent_asin` values
- Missing `parent_asin`
- Missing product titles
- Products below the minimum rating threshold

Validation results:

- Total products: 10,500
- Duplicate `parent_asin`: 0
- Missing `parent_asin`: 0
- Missing title: 0
- Products below 20 ratings: 0

The dataset contains missing price values for some products. These values are retained as missing and will be handled during the data-preprocessing stage rather than being artificially assigned.

---

## 8. Data Processing Principle

The original Amazon metadata is retained in the `data/raw/` directory and is not modified.

The selected dataset is stored separately under `data/processed/`.

This separation preserves the distinction between:

- Raw source data
- Project-generated processed data