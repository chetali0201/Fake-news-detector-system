# Project Report: Fake News Detector Using NLP and Machine Learning

## Abstract
The Fake News Detector is a web-based educational application that applies Natural Language Processing (NLP) and supervised machine learning to classify a news headline or article as FAKE or REAL based on patterns learned from a labeled dataset. The system cleans text, converts it into numerical features using Term Frequency–Inverse Document Frequency (TF-IDF), and compares Logistic Regression with a calibrated Passive Aggressive Classifier. The selected model is served through a Flask REST API and accessed from a React-based dashboard. Evaluation includes accuracy, precision, recall, F1-score, and a confusion matrix. The application is intended for learning and demonstration; its output is not definitive verification of factual claims.

## 1. Problem Statement
Online platforms contain a large volume of news and user-generated content, and manually reviewing every item can be difficult. A text-classification tool can help demonstrate how machine learning detects patterns in labeled examples. The project develops a web interface that accepts news text and returns a model-generated label with confidence and evaluation information.

## 2. Objectives
- Build a complete NLP-based text-classification workflow.
- Clean and prepare labeled news data.
- Convert text to numeric features using TF-IDF.
- Train and compare two supervised classification algorithms.
- Evaluate the selected model using held-out test data.
- Expose predictions through a Flask API.
- Build a responsive React dashboard to display predictions and metrics.
- Explain limitations, dataset bias, and the difference between model confidence and factual truth.

## 3. Technologies Used
- Python and pandas for data processing.
- scikit-learn for splitting, TF-IDF, model training, and evaluation.
- Logistic Regression and Passive Aggressive Classifier for classification.
- CalibratedClassifierCV to provide probability estimates for Passive Aggressive.
- Joblib to save and load the fitted model.
- Flask and Flask-CORS for the REST API.
- React and Vite for the frontend.
- Tailwind CSS for styling and Recharts for model comparison charts.

## 4. Methodology
### 4.1 Dataset
The system accepts either `Fake.csv` and `True.csv`, or a single `news.csv` with a `label` column and `text` and/or `title` columns. Labels are normalized to `FAKE` and `REAL`. The dataset source, license, collection method, and limitations should be documented in the final submission.

### 4.2 Preprocessing
The code reports missing values, removes duplicate rows, combines title and article text where available, strips HTML tags and URLs, removes punctuation, converts text to lowercase, and removes empty records or invalid labels. It also attempts to strip a common Reuters-style prefix that could act as a source shortcut in some datasets.

### 4.3 Train/validation/test split
The data is split using stratification into 64% training, 16% validation, and 20% test data, using a fixed random seed. Stratification preserves class proportions as closely as possible. The validation set is used to select a model; the test set is held out for final evaluation.

### 4.4 Feature extraction
TF-IDF represents text with weighted word and word-pair features. Words that are common across many documents receive less weight than terms that help distinguish documents. The vectorizer is part of the scikit-learn Pipeline, so it is fitted only on training data.

### 4.5 Models
**Logistic Regression:** a supervised linear classifier that estimates class probabilities from weighted text features.

**Passive Aggressive Classifier:** an online-learning-style linear classifier that updates its decision boundary when an example is misclassified or insufficiently separated. Because it does not directly provide probabilities, the implementation calibrates it with `CalibratedClassifierCV`.

### 4.6 Model selection and evaluation
Both models are trained on the training split and compared using validation F1-score. The model with the better validation F1-score is selected. Its held-out test results include accuracy, precision, recall, F1-score, and a confusion matrix. The actual results must be copied from `backend/models/metrics.json` after training on the chosen full dataset; no results should be invented.

- **Accuracy:** fraction of all predictions that are correct.
- **Precision:** among items predicted FAKE, the fraction that are actually labeled FAKE.
- **Recall:** among actual FAKE items, the fraction detected as FAKE.
- **F1-score:** harmonic mean of precision and recall.
- **Confusion matrix:** counts correct and incorrect predictions by class.

### 4.7 Application architecture
The React frontend sends input to the Flask `POST /api/predict` endpoint. Flask validates the text and uses the previously loaded model pipeline to produce a label, model confidence, class scores, and a disclaimer. The `GET /api/health` endpoint reports model availability, while `GET /api/metrics` supplies the model evaluation data for the dashboard.

## 5. Results
Complete this section after training on the selected real dataset. Record the dataset source, number of cleaned rows, train/validation/test counts, selected model, and values for accuracy, precision, recall, and F1-score. Include the confusion matrix and a screenshot of the running interface. Clearly mark any results from `sample_news.csv` as a smoke test only, not meaningful evidence of model quality.

## 6. Limitations
- The model learns correlations in the training data and does not independently verify claims against trusted sources.
- Dataset labels may be noisy or subjective.
- Source names, writing style, topic, and collection period may create shortcuts.
- A confidence score is not the probability that a claim is factually true.
- Performance may drop on new events, different languages, satire, or text outside the training distribution.
- The small synthetic sample file is unsuitable for measuring generalization.

## 7. Future Scope
- Add evidence retrieval from reputable sources and show citations for supporting or contradicting evidence.
- Test on independent datasets and perform temporal evaluation.
- Add multilingual processing, bias analysis, model monitoring, and automated tests.
- Improve accessibility, deployment reliability, and documentation.

## 8. Conclusion
This project demonstrates an end-to-end supervised NLP workflow, from text cleaning and TF-IDF feature extraction to model comparison, evaluation, API development, and a web dashboard. It provides a practical way to study machine learning integration in a full-stack application. Its predictions should be treated as model outputs requiring further verification, not as final judgments about truth.

## References
- scikit-learn documentation: https://scikit-learn.org/
- Flask documentation: https://flask.palletsprojects.com/
- React documentation: https://react.dev/
- Vite documentation: https://vite.dev/
- Dataset citation and source URL: add the exact dataset page and access date used for the final submission.
