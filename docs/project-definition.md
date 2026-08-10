# EthicCart — Project Definition

## 1. Problem Statement

Traditional product recommendation systems primarily optimize for factors such as price, popularity, ratings, and purchase behavior. They generally do not provide users with an ethical assessment of a product or recommend ethically preferable alternatives.

EthicCart aims to provide an AI-assisted ethical product evaluation and recommendation system.

## 2. Proposed Solution

EthicCart evaluates consumer products using structured ethical evidence and textual information. The system produces an ethical assessment, explains the major factors behind the decision, and recommends similar alternatives when a product is classified as unsuitable.

## 3. Project Objectives

- Evaluate products using multiple ethical dimensions.
- Provide BUY, DON'T BUY, or INSUFFICIENT EVIDENCE decisions.
- Use machine learning for ethical classification.
- Use NLP to analyze textual product/review information.
- Provide explainable predictions.
- Recommend ethically preferable alternatives.
- Incorporate relevant IEEE P7000-series principles into the ethical-system design.

## 4. Target Users

### Consumers

Users who want to consider ethical factors when purchasing products.

### Analysts / Administrators

Users responsible for examining product data and system performance.

### AI System

The ML/NLP components responsible for evaluation, explanation, and recommendation.

## 5. Core User Workflow

Search Product  
→ Select Product  
→ Ethical Evaluation  
→ BUY / DON'T BUY / INSUFFICIENT EVIDENCE  
→ Explanation  
→ Alternative Recommendations

## 6. Ethical Evaluation Dimensions

The project will investigate and operationalize relevant dimensions including:

- Transparency
- Privacy
- Safety
- Fairness
- Environmental impact
- Sustainability
- Human well-being
- Accountability
- Human oversight

The exact measurable indicators and their mapping to relevant IEEE P7000-series principles will be documented during the data and ethical-framework phases.

## 7. Machine Learning Strategy

Structured product and ethical evidence will be evaluated using traditional machine learning models, with XGBoost as a major candidate.

Baseline models will be evaluated before selecting the final model.

## 8. NLP Strategy

Textual information such as product reviews will be processed using an NLP pipeline.

A traditional TF-IDF approach will be used as a baseline, followed by an evaluation of DistilBERT for contextual text representation and ethical/sentiment signal extraction.

## 9. Explainable AI Strategy

SHAP will be used to understand feature contributions to model predictions. LIME may be used as a complementary local explanation technique where appropriate.

## 10. Recommendation Strategy

The system will use content-based similarity and ethical ranking to identify similar products with stronger ethical profiles.

## 11. Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- DistilBERT
- SHAP
- LIME
- Streamlit

## 12. Project Scope

The initial project will focus on consumer electronics, with an emphasis on products for which reliable sustainability and ethical evidence can be obtained.

## 13. Ethical Framework

The project will use an IEEE-informed ethical evaluation approach.

The project will not claim IEEE certification.

## 14. Important Limitation

The system is intended as an AI-assisted decision-support tool rather than an authoritative declaration of whether a company or product is morally good or bad.

Products with insufficient reliable evidence may receive an INSUFFICIENT EVIDENCE result rather than being automatically classified as unethical.