# quantum.py
# Quantum machine learning models built with Qiskit.
#
# What this file needs to do:
# 1. Reduce features to a small number (around 4 to 8), since each
#    feature typically becomes one qubit. Use PCA or feature selection.
# 2. Scale the reduced features to rotation angles (for example 0 to pi).
# 3. Build a quantum support vector classifier (QSVC) using a feature map
#    like ZZFeatureMap and a FidelityQuantumKernel. Build this one first.
# 4. Later, build a variational quantum classifier (VQC): a feature map plus
#    a trainable circuit like RealAmplitudes, trained with an optimizer.
# 5. Run on a local simulator first. Real hardware comes later, if at all.
#
# Models need the same fit() and predict_proba() interface as classical.py.
# Quantum models are slow, so expect to subsample the data at first.
#
# Suggested function: get_quantum_models, returning a dict of name to model
