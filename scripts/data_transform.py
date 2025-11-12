import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
from utils import log

# --------------------------------------
# Feature functions
# --------------------------------------
def compute_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily log returns for all price columns."""
    rets = np.log(df / df.shift(1))
    rets = rets.dropna(how="all")
    return rets

def compute_rolling_vol(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Compute rolling volatility (std dev of returns)."""
    return df.rolling(window).std()

def compute_zscore(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Compute rolling z-score of returns over a given window.
    Z_t = (r_t - mean_{t-window}) / std_{t-window}
    """
    mean = df.rolling(window).mean()
    std = df.rolling(window).std()
    z = (df - mean) / std
    return z

def compute_sma(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Compute rolling simple moving average (SMA) of returns.
    """
    sma = df.rolling(window).mean()
    return sma


# --------------------------------------
# Pipeline orchestration
# --------------------------------------
def transform():
    load_dotenv("globs.env")
    DATA_DIR = os.getenv("DATA_DIR")
    INPUT_PATH = os.path.join(DATA_DIR, "prices.csv")
    OUTPUT_PATH = os.path.join(DATA_DIR, "returns.csv")
    FEATURES_PATH = os.path.join(DATA_DIR, "features.csv")

    os.makedirs("logs", exist_ok=True)
    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LOG_FILE = os.path.join("logs", f"data_transform_{run_id}.log")

    log("===== DATA TRANSFORMATION START =====", LOG_FILE)
    log(f"Input: {INPUT_PATH}", LOG_FILE)

    # Load price data
    df = pd.read_csv(INPUT_PATH, parse_dates=["date"]).set_index("date").sort_index()
    log(f"Loaded {df.shape[0]} rows x {df.shape[1]} cols", LOG_FILE)

    # -----------------------------
    # Core transforms
    # -----------------------------
    rets = compute_log_returns(df)
    vol = compute_rolling_vol(rets)
    zscore = compute_zscore(df)
    sma = compute_sma(rets)

    # -----------------------------
    # Merge all feature sets
    # -----------------------------
    features = pd.concat({
        "RET": rets,
        "VOL": vol,
        "ROLLING_ZSCORE": zscore,
        "SMA": sma
    }, axis=1)

    # Save outputs
    rets.to_csv(OUTPUT_PATH)
    features.to_csv(FEATURES_PATH)

    log(f"[SAVED] returns -> {OUTPUT_PATH}", LOG_FILE)
    log(f"[SAVED] features -> {FEATURES_PATH} ({features.shape[0]} rows x {features.shape[1]} cols)", LOG_FILE)
    log("===== DATA TRANSFORMATION COMPLETE =====\n", LOG_FILE)

if __name__ == "__main__":
    transform()
