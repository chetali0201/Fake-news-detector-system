# Dataset setup
Download "Fake and Real News Dataset" (Kaggle, by Clément Bisaillon) and place **Fake.csv** and **True.csv** in this folder.
Both have columns `title,text,subject,date`; labels come from the file name.
Or provide your own `news.csv` with columns `text` (and/or `title`) and `label` (`REAL` / `FAKE`).

`sample_news.csv` is a tiny synthetic file ONLY for testing the app flow. Never use it to judge accuracy:
`python train_model.py --data ../data/sample_news.csv`
