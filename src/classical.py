# classical.py
# Classical machine learning models.
#
# What this file needs to do:
# 1. Logistic regression as the simple, interpretable baseline.
# 2. Support vector machine with an RBF kernel, the direct comparison
#    to the quantum kernel model.
# 3. A second SVM trained on the same reduced features the quantum
#    models use (same PCA size), so the head-to-head is fair.
# 4. A tree-based model, like gradient boosting, to test nonlinear patterns.
#
# Every model needs fit() and predict_proba() so evaluate.py can treat
# them identically. Scikit-learn models already work this way.
# Handle class imbalance (class_weight="balanced" or similar), since
# 20% declines are rare.
#
# Suggested function: get_classical_models, returning a dict of name to model
