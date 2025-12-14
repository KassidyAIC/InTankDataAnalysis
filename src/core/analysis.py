import pandas as pd

def process_dataframe(file_path):
    # """Example processing: add a 'Processed' column."""
    # df['Processed'] = True
    # return df
    df = load_log_file(file_path)
    df_pivot = df.pivot_table(
        index='TimeString',          # row index
        columns='VarName',           # each variable becomes a column
        values='VarValue',           # fill with VarValue
        aggfunc='first'              # if multiple entries per timestamp
    )

    # Optional: reset index so TimeString becomes a normal column
    df_pivot = df_pivot.reset_index()

    # Save to CSV
    df_pivot.to_csv("transformed_log.csv", index=False)
    return df_pivot 

def load_log_file(file_path):
    """Load CSV or Excel and return a DataFrame, skipping malformed lines."""
    if file_path.lower().endswith(".csv"):
        # skip lines with the wrong number of columns
        df = pd.read_csv(file_path, on_bad_lines='skip')
    else:
        df = pd.read_excel(file_path)
    return df