import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from tqdm import tqdm

def log(msg: str, log_file: str, level: str = "INFO"):
    """
    Append a timestamped message to a log file and echo via tqdm.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a") as f:
        f.write(line + "\n")
    tqdm.write(line)

def fetch_poly_api_key():
    """
    Load Polygon API key from polyio.env.
    """
    load_dotenv("polyio.env")
    API_KEY = os.getenv("POLY_API_KEY") or os.getenv("API_KEY")
    assert API_KEY, "POLY_API_KEY missing — check polyio.env"
    return API_KEY

def fetch_polygon_daily(ticker : str, START : str, END : str, API_KEY : str, adjusted : str = "true"):
    """
    Fetch OHLCV data via api endpoint.
    """
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
        f"{START}/{END}?adjusted={adjusted}&sort=asc&limit=50000&apiKey={API_KEY}"
    )
    r = requests.get(url)
    
    if r.status_code != 200:
        print(f"[ERR] {ticker}: {r.status_code}")
        return None
    
    js = r.json()
    if "results" not in js:
        return None
    
    df = pd.DataFrame(js["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={
        "o":"open", "h":"high", "l":"low", "c":"close", "v":"volume"
    })
    
    return df[["date","close"]]

def download_stitched(ticker: str, START: str, END: str, API_KEY: str, adjusted: str = "true"):
    """
    Download a ticker, stitching together any known renames
    """
    load_dotenv("globs.env")
    mapping_str = os.getenv("MAPPINGS")
    
    # Parse mapping (e.g. META:FB@2022-06-09)
    mapping = {}
    if mapping_str:
        for entry in mapping_str.split(","):
            new, rest = entry.split(":")
            old, date = rest.split("@")
            mapping[new.strip()] = (old.strip(), date.strip())

    if ticker in mapping:
        old_ticker, cut_date = mapping[ticker]
        df_old = fetch_polygon_daily(old_ticker, START, cut_date, API_KEY, adjusted)
        cut_next = (pd.to_datetime(cut_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        df_new = fetch_polygon_daily(ticker, cut_next, END, API_KEY, adjusted)
        df = pd.concat([df_old, df_new]).drop_duplicates("date").sort_values("date")
    else:
        df = fetch_polygon_daily(ticker, START, END, API_KEY, adjusted)

    return df
