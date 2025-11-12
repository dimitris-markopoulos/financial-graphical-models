import os
import time
import requests
import json
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
from utils import *

def fetch_data():
    """
    Fetch data - load tickers and merge into one file.
    """
    load_dotenv("globs.env")
    DATA_DIR = os.getenv("DATA_DIR")
    START_DATE = os.getenv("START_DATE")
    END_DATE = os.getenv("END_DATE")
    TICKERS = os.getenv("TICKERS").split(",")
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    api_key = fetch_poly_api_key()

    run_id = datetime.now().strftime("%Y-%m-%d")
    LOG_FILE = os.path.join("logs", f"data_download_{run_id}.log")

    log("===== DATA DOWNLOAD SESSION START =====", LOG_FILE)
    log(f"Run parameters: START={START_DATE}, END={END_DATE}", LOG_FILE)
    log(f"Tickers: {', '.join(TICKERS)}", LOG_FILE)
    log("----------------------------------------", LOG_FILE)


    df = None
    for ticker in tqdm(TICKERS):
        try:
            x = download_stitched(
                ticker=ticker,
                START=START_DATE,
                END=END_DATE,
                API_KEY=api_key,
                adjusted="true"
            ).rename(columns={"close": f"{ticker}_close"})

            if x is None or x.empty:
                log(f"[FAIL] {ticker}: No data returned", LOG_FILE, "WARN")
                continue

            if df is None:
                df = x
            else:
                df = pd.merge(df, x, on="date", how="outer")

            log(f"[OK] {ticker}: Downloaded {len(x)} rows", LOG_FILE)

        except Exception as e:
            log(f"[ERR] {ticker}: {e}", LOG_FILE, "ERROR")

    if df is None or df.empty:
        log("[ABORT] No data collected — nothing to save", LOG_FILE, "ERROR")
        return

    out_path = os.path.join(DATA_DIR, "prices.csv")
    df.to_csv(out_path, index=False)
    log(f"[SAVED] {out_path} ({df.shape[0]} rows x {df.shape[1]} cols)", LOG_FILE)
    log("===== DATA DOWNLOAD SESSION COMPLETE =====\n", LOG_FILE)

if __name__=="__main__":
    fetch_data()