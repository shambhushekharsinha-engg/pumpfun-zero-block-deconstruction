import nbformat as nbf

nb = nbf.v4.new_notebook()

markdown_intro = """# Solana Sniper Bot Reverse-Engineering
This notebook contains the complete pipeline for the Solana Sniper Bot Kaggle competition.
It includes Data Generation, Behavioral Analysis, Feature Engineering, Model Training, and Replica Backtesting.
"""

code_part1 = open("src/generate_sample_data.py").read() + "\ngenerate_synthetic_dataset()"
code_part2 = open("src/part1_behavioral_analysis.py").read() + "\nrun_behavioral_analysis()"
code_part3 = open("src/part2_feature_engineering.py").read() + "\nrun_feature_engineering_and_modeling()"
code_part4 = open("src/part3_replica_backtest.py").read() + "\nrun_replica_backtest()"

nb['cells'] = [
    nbf.v4.new_markdown_cell(markdown_intro),
    nbf.v4.new_code_cell(code_part1),
    nbf.v4.new_code_cell(code_part2),
    nbf.v4.new_code_cell(code_part3),
    nbf.v4.new_code_cell(code_part4)
]

nbf.write(nb, 'solana_sniper_bot_replica.ipynb')
print("Notebook created.")
