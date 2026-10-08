"""Runs the pipeline end to end: python run.py"""

from src.classical import get_classical_models
from src.data import get_prices, load_business_sheet, load_config
from src.evaluate import run_model
from src.prepare import build_dataset, make_labels, make_market_features


def main():
    cfg = load_config()
    lab = cfg["label"]

    print("1. Pulling prices")
    close, volume = get_prices(cfg["tickers"], cfg["start_date"], cfg["end_date"])

    print("2. Loading business sheet")
    load_business_sheet(cfg["business_sheet"])

    print("3. Building labels and features")
    labels = make_labels(close, lab["horizon_days"], lab["drop_threshold"], lab["rule"])
    data = build_dataset(make_market_features(close, volume), labels)

    print("\nSanity check: decline events per company")
    summary = data.groupby("ticker")["label"].agg(rows="count", events="sum")
    print(summary.astype(int), "\n")

    print("4. Classical baselines on market-only features")
    ev = cfg["evaluation"]
    for name, model in get_classical_models(ev["quantum_features"]).items():
        results = run_model(model, data, ev["n_splits"], lab["horizon_days"])
        print(f"\n{name}")
        print(results.round(3).to_string(index=False) if len(results) else "  no valid folds")

    # Quantum models are slower. Uncomment once classical results look sensible.
    # from src.quantum import get_quantum_models
    # for name, model in get_quantum_models(ev["quantum_features"]).items():
    #     print(name, run_model(model, data, ev["n_splits"], lab["horizon_days"]))


if __name__ == "__main__":
    main()
