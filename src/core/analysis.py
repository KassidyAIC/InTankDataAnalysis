import pandas as pd

def load_log_file(file_path):
    """Load CSV or Excel and return a DataFrame, skipping malformed lines."""
    if file_path.lower().endswith(".csv"):
        # skip lines with the wrong number of columns
        df = pd.read_csv(file_path, on_bad_lines='skip')
    else:
        df = pd.read_excel(file_path)
    return df

def process_dataframe(df):
    """Example processing: add a 'Processed' column."""
    df['Processed'] = True
    return df