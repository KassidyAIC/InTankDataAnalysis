from src.config.app_config import AppConfig
from src.config.sequence_config import load_tank_seq_map
import pandas as pd
import re

def process_dataframe(file_path, app_config: AppConfig) -> pd.DataFrame:
    df = load_log_file(file_path)

    # Only select the rows corresponding to sequence steps
    mask = df['VarName'].str.contains(r'DB_CTRL\.Tanks\[\d+\]\.Seq\.Step')
    seq_df = df[mask].copy()

    # Extract tank number
    seq_df['Tank'] = seq_df['VarName'].apply(lambda x: int(re.search(r'\[(\d+)\]', x).group(1)))

    # Use VarValue as SeqStep
    seq_df['SeqStep'] = seq_df['VarValue']
    seq_df["SeqStep"] = pd.to_numeric(seq_df["SeqStep"], errors="coerce")
    tank_seq_step_map = load_tank_seq_map()
    seq_df["SeqStepName"] = seq_df["SeqStep"].map(tank_seq_step_map).fillna("Unknown")
    seq_df = seq_df[seq_df["SeqStepName"] != "Unknown"] # remove logs for sequence unknown sequence numbers

    seq_df["TankName"] = seq_df["Tank"].map(app_config.tank_name_map()).fillna("")
    seq_df["BallastGroup"] = seq_df["Tank"].map(app_config.ballast_group_map()).fillna(0)
    seq_df = seq_df[seq_df["TankName"] != ""] # remove logs for tanks that do not exist
    
    out = seq_df[['TimeString', 'BallastGroup', 'Tank', 'TankName', 'SeqStep', 'SeqStepName']].copy()
    out = out.rename(columns={
        "Tank": "Tank Number",
        "TankName": "Tank Name",
        "SeqStep": "Tank Sequence Step Number",
        "SeqStepName": "Tank Sequence Step Name",
    })

    out.to_csv("transformed_seq_log.csv", index=False)
    return out

def load_log_file(file_path):
    """Load CSV or Excel and return a DataFrame, skipping malformed lines."""
    if file_path.lower().endswith(".csv"):
        # skip lines with the wrong number of columns
        df = pd.read_csv(file_path, on_bad_lines='skip')
    else:
        df = pd.read_excel(file_path)
    return df