# evaluate.py
# Shared testing code. Every model, classical and quantum, goes through
# this exact file so the comparison stays fair.
#
# What this file needs to do:
# 1. Create walk-forward splits: train on earlier dates, test on later dates.
# 2. Purge the gap between train and test. Training data must stop one
#    horizon (30 trading days) before each test period starts. Otherwise,
#    training labels can see prices inside the test period.
# 3. Train a model on each split and record its predicted probabilities.
# 4. Score each split on recall (declines caught), precision (how often
#    warnings were right), PR-AUC, and Brier score (calibration).
#    Don't use plain accuracy. Declines are rare, so it's misleading.
# 5. Break results down by company and by time period.
# 6. Record training time so classical and quantum effort can be compared.
# 7. Make quick charts of predicted probability over time with actual
#    declines marked.
#
# Suggested functions: walk_forward_splits, score, run_model, plot_forecasts
