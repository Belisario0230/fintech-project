import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
import os

def run_pipeline():
    # 1. Extracción con verificación de directorio
    os.makedirs("/app/data/raw", exist_ok=True)
    tickers = ["AAPL", "MSFT", "GOOG"]
    data = yf.download(tickers, start="2023-01-01", end="2023-12-31")["Close"]
    data.to_parquet("/app/data/raw/stock_data.parquet")

    # 2. Transformación
    df = pd.read_parquet("/app/data/raw/stock_data.parquet")
    df = df.reset_index().melt(id_vars='Date', var_name='ticker', value_name='Price')
    df["Daily_Return"] = df.groupby("ticker")["Price"].pct_change()

    # 3. Carga
    engine = create_engine("postgresql://user:pass@postgres:5432/fintech")
    df.to_sql("stocks", engine, if_exists="replace", index=False)
    print("✅ Pipeline ejecutado correctamente!")

if __name__ == "__main__":
    run_pipeline()
