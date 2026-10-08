"""Classical classifiers. Every model has fit() and predict_proba()."""

from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def get_classical_models(quantum_features=4):
    return {
        "logistic": make_pipeline(
            StandardScaler(),
            LogisticRegression(class_weight="balanced", max_iter=1000)),
        "svm": make_pipeline(
            StandardScaler(),
            SVC(kernel="rbf", probability=True, class_weight="balanced")),
        # Same reduced inputs as the quantum models, for a fair head-to-head
        "svm_reduced": make_pipeline(
            StandardScaler(),
            PCA(n_components=quantum_features),
            SVC(kernel="rbf", probability=True, class_weight="balanced")),
        "gradient_boosting": HistGradientBoostingClassifier(
            class_weight="balanced"),
    }
