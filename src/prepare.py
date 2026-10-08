# prepare.py
# Turns raw data into labels and features the models can use.
#
# What this file needs to do:
# 1. Build the label: 1 if a stock falls at least the threshold (default 20%)
#    over the next horizon (default 30 trading days), otherwise 0.
#    Support both rules from config.yaml: end_of_window and any_point.
#    Rows near the end, where the future isn't known yet, must be left blank.
# 2. Build tier 1 features (market only): recent returns, volatility,
#    volume changes, and drawdown from recent highs.
# 3. Build tier 2 features (company): cash runway, revenue growth, and
#    event scores from the business sheet.
# 4. Build tier 3 features (external): rates, VIX, credit spreads, and
#    returns of related sector ETFs.
# 5. Combine everything into one table with one row per (date, ticker).
#
# Key rule: a feature on date t may only use information public on or before t.
# Financials count from their filing date, not the quarter end. An announcement
# released after the close counts toward the next trading day.
#
# Suggested functions: make_labels, make_market_features,
# make_company_features, make_external_features, build_dataset
