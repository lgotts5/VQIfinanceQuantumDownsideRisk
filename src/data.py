"""Loads every raw input: stock prices, macro series, and the business sheet."""

from pathlib import Path

import pandas as pd
import yaml

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"

# Columns the code expects in each tab of the finance team's spreadsheet.
REQUIRED_COLUMNS = {
    "Companies": ["Ticker", "Name", "Listing date", "Include"],
    "Events": ["Event ID", "Ticker", "Announcement date", "Release timing",
               "First tradable date", "Category", "Validation status"],
    "Financials": ["Ticker", "Period end", "Filing date", "Cash", "Revenue"],
}


def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def get_prices(tickers, start, end=None):
    """Daily adjusted close and volume. Returns (close, volume), dates x tickers."""
    import yfinance as yf

    raw = yf.download(tickers, start=start, end=end,
                      auto_adjust=True, progress=False)
    return raw["Close"], raw["Volume"]


def get_macro(series_ids, start):
    """Pulls each FRED series and joins them into one daily table."""
    frames = []
    for name, series in series_ids.items():
        df = pd.read_csv(FRED_URL.format(series=series),
                         index_col=0, parse_dates=True, na_values=".")
        df.columns = [name]
        frames.append(df)
    macro = pd.concat(frames, axis=1)
    return macro.loc[start:].ffill()


def load_business_sheet(path):
    """Loads the Excel tabs and flags problems right away."""
    path = Path(path)
    if not path.exists():
        print(f"Business sheet not found at {path}. Skipping.")
        return None

    sheets = pd.read_excel(path, sheet_name=None)
    for tab, columns in REQUIRED_COLUMNS.items():
        if tab not in sheets:
            print(f"Warning: tab '{tab}' is missing.")
            continue
        missing = [c for c in columns if c not in sheets[tab].columns]
        if missing:
            print(f"Warning: '{tab}' is missing columns {missing}.")

    events = sheets.get("Events")
    if events is not None and "Event ID" in events:
        dupes = events["Event ID"][events["Event ID"].duplicated()]
        if len(dupes):
            print(f"Warning: duplicate Event IDs {list(dupes)}.")
    return sheets
