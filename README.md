# Fake News Detector Using NLP and Machine Learning

A college-level web application that predicts whether a news headline/article resembles the **FAKE** or **REAL** examples in a labeled training dataset. It uses TF-IDF text features and compares Logistic Regression with a calibrated Passive Aggressive Classifier. A Flask API serves predictions to a React dashboard.

> **Important limitation:** this is a text-classification demonstration, not a fact-checking service. A prediction does not prove that a claim is true or false. Dataset bias, source patterns, context, and changing events can affect results.

## Project structure

```text
fake-news-detector/
├── backend/
│   ├── app.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── requirements.txt
│   ├── .env.example
│   └── models/                 # generated after training; not included
├── data/
│   ├── README.md
│   └── sample_news.csv         # synthetic smoke-test data only
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── PROJECT_REPORT.md
├── VIVA_QUESTIONS.md
└── .gitignore
```

## Requirements

- Python 3.10+ recommended
- Node.js 18+
- npm
- A labeled dataset. The `data/sample_news.csv` file is tiny and synthetic; do not use its scores as evidence of real-world performance.

## 1. Add the dataset

Download a reputable, labeled fake/real news dataset and follow its license/terms. For the commonly used Kaggle Fake and Real News Dataset, put `Fake.csv` and `True.csv` in the root `data/` folder. Alternatively, provide `data/news.csv` with a `label` column and a `text` and/or `title` column. Labels should be `FAKE` or `REAL`.

## 2. Start the Flask backend (Windows PowerShell)

Open a terminal in the project root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python train_model.py
python app.py
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again. Training may take some time on a large dataset. It creates `backend/models/model_pipeline.joblib`, `tfidf_vectorizer.joblib`, and `metrics.json`.

To try only the application flow with synthetic data, run `python train_model.py --data ..\data\sample_news.csv`. This is for smoke testing only and produces meaningless evaluation metrics. Retrain on the full labeled dataset before evaluating the project.

The API normally runs at `http://127.0.0.1:5000`.

## 3. Start the React frontend

Keep the backend terminal running. Open a second terminal at the project root:

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Open the local URL Vite prints, usually `http://localhost:5173`.

The frontend reads `VITE_API_BASE_URL` from `frontend/.env`. Default: `http://localhost:5000`. Restart Vite after changing `.env`.

## API endpoints

- `GET /api/health` — server status and whether the trained model is loaded.
- `POST /api/predict` — JSON body: `{"text":"A headline with at least three words"}`.
- `GET /api/metrics` — selected model, dataset split sizes, model comparison and selected test metrics.

## Training and evaluation approach

1. Load the CSV file(s), report missing values, normalize labels, clean text, and remove duplicate/empty records.
2. Make stratified train/validation/test splits (64%/16%/20%).
3. Train TF-IDF + Logistic Regression and TF-IDF + calibrated Passive Aggressive pipelines.
4. Select the model with the best validation F1-score.
5. Report the selected model's held-out test metrics and save the pipeline and metrics as files.

TF-IDF is inside each scikit-learn pipeline, so its vocabulary and IDF weights are fitted from training data rather than the validation/test sets.

## Verification checklist

- [ ] `GET http://127.0.0.1:5000/api/health` returns JSON.
- [ ] Health response reports `model_loaded: true` after training.
- [ ] Frontend status badge shows the backend is online and model loaded.
- [ ] Empty text is rejected by the frontend.
- [ ] Text shorter than three words is rejected.
- [ ] Sample input can be submitted and a prediction is shown.
- [ ] Clear resets the input and result.
- [ ] Metrics match `backend/models/metrics.json`.
- [ ] Stop Flask: frontend reports a connection error.
- [ ] Test on a narrow/mobile viewport for layout issues.

## Troubleshooting

- **`Model not trained` / HTTP 503:** run `python train_model.py` from `backend` with the dataset in `../data`.
- **Backend offline:** ensure `python app.py` is still running and `VITE_API_BASE_URL` points to the Flask port.
- **CORS error:** edit `backend/.env` and set `CORS_ORIGINS=http://localhost:5173`; restart Flask.
- **Missing module:** activate the backend virtual environment and run `pip install -r requirements.txt`.
- **npm/build error:** verify Node.js 18+ with `node --version`, then run `npm install` in `frontend`.

## Future scope

- Use verified sources and evidence retrieval rather than text style alone.
- Add multilingual support, source attribution, temporal evaluation, and model monitoring.
- Evaluate on an external dataset and report class-wise metrics and limitations.
- Add tests, deployment configuration, accessibility checks, and a privacy-conscious logging policy.
