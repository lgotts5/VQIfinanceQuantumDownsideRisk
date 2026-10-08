# run.py
# Runs the whole pipeline in order with one command: python run.py
#
# What this file needs to do:
# 1. Load config.yaml.
# 2. Pull prices and macro data, and load the business sheet (data.py).
# 3. Build labels and features (prepare.py).
# 4. Print a sanity check: rows and decline events per company.
#    If a company has almost no declines, flag it.
# 5. Run the classical models through evaluate.py and print results.
# 6. Run the quantum models the same way, once classical results look sensible.
# 7. Save results and charts to a results/ folder.
#
# Keep this file short. It should only call functions from src/,
# not contain any real logic itself.
