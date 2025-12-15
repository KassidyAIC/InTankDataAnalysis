from __future__ import annotations

import pandas as pd
from importlib import resources

_STEP_MAP_CACHE: dict[int, str] | None = None

def load_tank_seq_map() -> dict[int, str]:
    global _STEP_MAP_CACHE
    if _STEP_MAP_CACHE is not None:
        return _STEP_MAP_CACHE

    with resources.files("src.config.data").joinpath("sequence_steps_tank.csv").open("rb") as f:
        df = pd.read_csv(f)

    # normalize + build map
    df["SeqStep"] = df["SeqStep"].astype(int)
    df["Name"] = df["Name"].astype(str)

    _STEP_MAP_CACHE = dict(zip(df["SeqStep"], df["Name"]))
    return _STEP_MAP_CACHE