# EthicCart — Data Dictionary

## Products

| Field | Description | Source |
|---|---|---|
| product_id | Unified product identifier | Derived |
| product_name | Product name | Amazon |
| brand | Product manufacturer/brand | Amazon |
| category | Product category | Amazon |
| price | Product price | Amazon |
| average_rating | Average product rating | Amazon |
| rating_count | Number of ratings | Amazon |
| features | Product feature list | Amazon |
| description | Product description | Amazon |
| product_details | Structured product details | Amazon |

## Reviews

| Field | Description | Source |
|---|---|---|
| review_id | Unique review identifier | Derived |
| product_id | Unified product identifier | Derived |
| user_id | Reviewer identifier | Amazon |
| rating | Review rating | Amazon |
| title | Review title | Amazon |
| review_text | Review body | Amazon |
| timestamp | Review timestamp | Amazon |
| verified_purchase | Whether purchase was verified | Amazon |
| helpful_vote | Number of helpful votes | Amazon |

## Certification Evidence

| Field | Description | Source |
|---|---|---|
| product_id | Unified product identifier | Derived |
| epeat_certified | Whether product is listed in EPEAT | EPEAT |
| epeat_tier | EPEAT tier where applicable | EPEAT |
| epeat_version | EPEAT criteria/version | EPEAT |
| epeat_status | Current/archived status | EPEAT |
| tco_certified | Whether product is TCO Certified | TCO |
| tco_generation | TCO certification generation | TCO |
| tco_status | Certification status | TCO |
| source | Evidence source | Derived |
| source_url | Evidence reference | Derived |
| evidence_date | Date evidence was collected | Derived |
