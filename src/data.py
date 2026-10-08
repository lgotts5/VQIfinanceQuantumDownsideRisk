# data.py
# Loads every raw input the project uses. No cleaning or features here.
#
# What this file needs to do:
# 1. Read config.yaml so tickers, dates, and file paths aren't hardcoded.
# 2. Pull daily adjusted close prices and trading volume for each ticker
#    and benchmark ETF (yfinance works for this).
# 3. Pull macro series from FRED: interest rates, VIX, credit spreads.
#    Forward-fill gaps, since some series skip weekends and holidays.
# 4. Load the finance team's Excel file (Companies, Events, Financials tabs).
# 5. Check the Excel file on load and print clear warnings for missing tabs,
#    missing columns, blank dates, invalid categories, or duplicate Event IDs.
#
# Suggested functions: load_config, get_prices, get_macro, load_business_sheet
