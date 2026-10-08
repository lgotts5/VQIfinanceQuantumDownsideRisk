"""Builds the decline labels and the model features."""

import numpy as np
import pandas as pd


def make_labels(close, horizon=30, threshold=0.20, rule="end_of_window"):
    """1 if the stock falls at least `threshold` over the next `horizon` days.

    end_of_window: compares the price `horizon` days ahead to today.
    any_point: compares the lowest price in the next `horizon` days to today.
    Rows near the end, where the future is unknown, stay NaN.
    """
    if rule == "end_of_window":
        future = close.shift(-horizon)
    elif rule == "any_point":
        # Lowest close from day t+1 through day t+horizon
        future = close[::-1].rolling(horizon).min()[::-1].shift(-1)
    else:
        raise ValueError("rule must be end_of_window or any_point")

    change = future / close - 1
    labels = (change <= -threshold).astype(float)
    return labels.where(change.notna())


def make_market_features(close, volume):
    """Tier 1 features. Each uses only data up to and including day t."""
    daily = close.pct_change()
    features = {
        "return_5d": close.pct_change(5),
        "return_21d": close.pct_change(21),
        "volatility_21d": daily.rolling(21).std() * np.sqrt(252),
        "volume_ratio": volume / volume.rolling(21).mean(),
        "drawdown_63d": close / close.rolling(63).max() - 1,
    }
    return to_long(features)


def to_long(wide_tables):
    """Turns {name: dates x tickers} tables into one (date, ticker) table."""
    long = pd.concat({name: t.stack() for name, t in wide_tables.items()}, axis=1)
    long.index.names = ["date", "ticker"]
    return long


def build_dataset(features, labels):
    """Joins features with labels and drops rows missing either."""
    target = labels.stack().rename("label")
    target.index.names = ["date", "ticker"]
    data = features.join(target, how="inner")
    return data.dropna().sort_index()

# TODO tier 2: company features from the business sheet (events, financials)
# TODO tier 3: macro and related-group features
