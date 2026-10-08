# Predicting Downside Risk in Quantum Computing Stocks

VQI Finance project comparing classical and quantum classifiers for predicting
whether a quantum computing stock falls at least 20% over the next 30 trading days.
## About the project

This project tests whether we can predict sharp declines in quantum computing
stocks. For each company, we predict whether its stock will fall at least 20%
over the next 30 trading days.

Predictions draw on four kinds of information. These are market behavior,
company financials, announcements and technical milestones, and broader
economic conditions. The finance team builds and scores the company dataset.
The technical team builds the pipeline, models, and testing framework.

We compare classical machine learning models with quantum classifiers built
in Qiskit, using the same data and the same tests. Whether quantum methods
add value is a research question, not an assumption.

As an extension, we will study whether declines in quantum stocks spill over
into related sectors like semiconductors, AI, and cloud computing.

## Setup

```
git clone <repo-url>
cd quantum-downside-risk
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Project layout

| File | Purpose |
|---|---|
| `config.yaml` | Tickers, threshold, horizon, dates. All team decisions live here. |
| `src/data.py` | Pulls prices and macro data, loads the business Excel sheet |
| `src/prepare.py` | Builds the decline labels and model features |
| `src/evaluate.py` | Walk-forward splits, metrics, quick charts |
| `src/classical.py` | Logistic regression, SVM, gradient boosting |
| `src/quantum.py` | Quantum support vector classifier (VQC to follow) |
| `run.py` | Runs the pipeline end to end |

The finance team's spreadsheet goes in `data/business/business_data.xlsx`.

## Team rules

1. Never commit directly to `main`. Make a branch, push it, open a pull request.
2. Never commit API keys or large data files.
3. Every model uses the same splits and the same `evaluate.py`. This keeps the
   classical vs quantum comparison fair.
4. Features may only use information public on or before the forecast date.
