"""Quantum classifiers. Same fit() and predict_proba() interface as classical.py.

Each feature becomes one qubit, so inputs are reduced with PCA first.
Runs on a local simulator by default.
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def get_quantum_models(quantum_features=4):
    from qiskit.circuit.library import ZZFeatureMap
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit_machine_learning.kernels import FidelityQuantumKernel

    feature_map = ZZFeatureMap(feature_dimension=quantum_features, reps=2)
    kernel = FidelityQuantumKernel(feature_map=feature_map)

    return {
        "qsvc": make_pipeline(
            StandardScaler(),
            PCA(n_components=quantum_features),
            MinMaxScaler(feature_range=(0, np.pi)),  # scale to rotation angles
            QSVC(quantum_kernel=kernel, probability=True,
                 class_weight="balanced")),
    }

# TODO: add the variational quantum classifier (VQC) once QSVC results are in.
