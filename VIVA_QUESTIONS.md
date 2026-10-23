# Viva Preparation: Fake News Detector Using NLP

## Short project explanation
“My project is a web-based Fake News Detector that uses NLP and supervised machine learning. It cleans news text, converts it into TF-IDF features, and compares Logistic Regression with a calibrated Passive Aggressive Classifier. The selected model is saved using Joblib and served through a Flask API. A React dashboard lets the user submit text and view the predicted label, model confidence, and evaluation metrics. The system demonstrates text classification; it does not independently prove whether a claim is true.”

## Common viva questions and answers

### 1. What is NLP?
Natural Language Processing is a field of AI that helps computers process and analyze human language.

### 2. Why did you choose this project?
It combines data preprocessing, NLP, machine learning evaluation, API development, and frontend integration in one practical project.

### 3. What is supervised learning?
Supervised learning trains a model using examples that already have labels. Here, news articles are labeled FAKE or REAL.

### 4. What is TF-IDF?
TF-IDF stands for Term Frequency–Inverse Document Frequency. It assigns higher weights to words that are important in a document but less common across the whole collection.

### 5. Why can't a model directly learn raw text?
Most classical machine-learning algorithms need numerical input. TF-IDF converts text into numeric feature vectors.

### 6. What is Logistic Regression?
Despite its name, Logistic Regression is commonly used for classification. It estimates class probabilities from a weighted combination of input features.

### 7. What is a Passive Aggressive Classifier?
It is a linear classifier inspired by online learning. It updates its parameters when training examples indicate that the current decision boundary is inadequate.

### 8. Why calibrate Passive Aggressive?
The base classifier does not provide probability estimates. Calibration maps its decision scores to estimated class probabilities, though these still do not represent factual truth.

### 9. What is data leakage?
Data leakage occurs when information from validation or test data improperly influences training. Keeping TF-IDF inside a Pipeline ensures it learns vocabulary and IDF weights from training text only.

### 10. Why use train, validation, and test sets?
Training data fits the model, validation data selects between candidate models, and test data estimates final performance on held-out examples.

### 11. Why use stratified splitting?
It preserves the relative proportion of each class across the splits, helping evaluation remain representative when class counts differ.

### 12. What is accuracy?
Accuracy is the number of correct predictions divided by the total number of predictions.

### 13. What is precision?
Precision for FAKE is TP / (TP + FP): of the items predicted FAKE, how many are labeled FAKE in the dataset.

### 14. What is recall?
Recall for FAKE is TP / (TP + FN): of all items labeled FAKE, how many the model detected.

### 15. What is F1-score?
F1 is the harmonic mean of precision and recall. It is useful when both false positives and false negatives matter.

### 16. What does a confusion matrix show?
It shows counts of correct and incorrect predictions for each actual and predicted class. In this project the class order is FAKE, REAL.

### 17. What does model confidence mean?
It is the model’s estimated confidence in its predicted class based on the learned patterns. It is not proof and not necessarily the probability that the news is true.

### 18. Why use Flask?
Flask provides a lightweight way to expose the trained Python model through HTTP endpoints that the React frontend can call.

### 19. What is an API endpoint?
An endpoint is a URL path that provides a defined service. This project uses `/api/health`, `/api/predict`, and `/api/metrics`.

### 20. Why save the model with Joblib?
Joblib serializes fitted Python objects such as scikit-learn pipelines so the application can load the trained model without retraining on every request.

### 21. Why keep the vectorizer in a Pipeline?
The Pipeline keeps text vectorization and classification together and helps prevent preprocessing inconsistencies and data leakage.

### 22. What is CORS?
Cross-Origin Resource Sharing is a browser security mechanism. Flask-CORS allows the frontend origin, such as `http://localhost:5173`, to call the backend at another port.

### 23. What is the role of React?
React builds the interactive user interface: text input, prediction result, status badge, metrics, and charts.

### 24. What are the project limitations?
The model learns patterns from its dataset, which can contain noisy labels and source or topic bias. It cannot independently verify claims and may perform poorly on new events or different writing styles.

### 25. How would you improve it?
I would add retrieval from reliable sources, citations, independent test datasets, multilingual support, bias checks, temporal evaluation, and monitoring.

## Before your viva
- Train on the full labeled dataset and keep the actual `metrics.json`.
- Be ready to explain your real test results; do not memorize invented scores.
- Open the working frontend and demonstrate one prediction.
- Explain the confusion matrix and why the sample CSV is not suitable for final evaluation.
- Be honest that the model is a text classifier, not a complete fact-checking system.
