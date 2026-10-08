"""Walk-forward splits, metrics, and quick charts. Shared by every model."""

import numpy as np
import pandas as pd
from sklearn.metrics import (average_precision_score, brier_score_loss,
                             precision_score, recall_score)


def walk_forward_splits(dates, n_splits=4, horizon=30):
    """Expanding-window splits with a purge gap.

    Training stops `horizon` trading days before each test block starts,
    so no training label can see prices inside the test period.
    """
    unique = np.sort(pd.Index(dates).unique())
    blocks = np.array_split(unique, n_splits + 1)
    for i in range(1, n_splits + 1):
        test_dates = blocks[i]
        cutoff_pos = np.searchsorted(unique, test_dates[0]) - horizon
        if cutoff_pos <= 0:
            continue
        train_dates = unique[:cutoff_pos]
        train_idx = np.where(np.isin(dates, train_dates))[0]
        test_idx = np.where(np.isin(dates, test_dates))[0]
        yield train_idx, test_idx


def score(y_true, prob, cutoff=0.5):
    pred = (prob >= cutoff).astype(int)
    return {
        "recall": recall_score(y_true, pred, zero_division=0),
        "precision": precision_score(y_true, pred, zero_division=0),
        "pr_auc": average_precision_score(y_true, prob),
        "brier": brier_score_loss(y_true, prob),
        "n_events": int(y_true.sum()),
    }


def run_model(model, data, n_splits=4, horizon=30):
    """Trains and scores one model on every split. Returns one row per split."""
    X = data.drop(columns="label").values
    y = data["label"].values.astype(int)
    dates = data.index.get_level_values("date")

    rows = []
    for fold, (tr, te) in enumerate(walk_forward_splits(dates, n_splits, horizon)):
        if y[tr].sum() == 0 or y[te].sum() == 0:
            print(f"  fold {fold}: skipped, no decline events in train or test")
            continue
        model.fit(X[tr], y[tr])
        prob = model.predict_proba(X[te])[:, 1]
        rows.append({"fold": fold, **score(y[te], prob)})
    return pd.DataFrame(rows)


def plot_forecasts(dates, prob, label, ticker, path=None):
    """Predicted probability over time with actual declines marked."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dates, prob, label="Predicted probability")
    hits = label == 1
    ax.scatter(np.asarray(dates)[hits], np.asarray(prob)[hits],
               color="red", s=12, label="Actual 20% decline")
    ax.set_title(ticker)
    ax.legend()
    if path:
        fig.savefig(path, bbox_inches="tight")
    return fig
