# stock data 수집 서비스
# conda activate service-stock
# libs: yfinance, flask, python-dotenv
import os

import yfinance as yf
from flask import Flask, request
from dotenv import load_dotenv

from utils import db

app = Flask(__name__)

@app.route("/service/stock", methods=["POST"])
def collect_stock_prices():
    """
        yahoo finance를 통해 종가를 DB(service.stock, OLTP)에 저장하는 서비스
        1. json을 포함하는 request
    """
    if request.method == "POST":
        tickers = request.get_json().get("tickers", ["SPY"])

        sql = f"""
                BEGIN;
                DROP TABLE IF EXISTS service.stock;
                CREATE TABLE service.stock (
                    ts timestamp,
                    close FLOAT,
                    ticker VARCHAR
                );
            """
        for ticker in tickers:
            raw_df = yf.download([ticker])
            for ts, row in raw_df.iterrows():
                sql += f"""
                        INSERT INTO service.stock (ts, close, ticker)
                        VALUES ('{ts.strftime("%Y-%m-%d %H:%M:%S")}', {row.Close}, '{ticker}');
                    """

        conn = db.get_connector()
        cur = conn.cursor()
        cur.execute(sql)
        cur.execute("END;")
    else:
        raise Exception("[ERROR] request must be POST method")

    return "done"

if __name__=="__main__":
    load_dotenv()
    LOCAL_HOST = os.environ.get("LOCAL_HOST")
    INBOUND_PORT = os.environ.get("INBOUND_PORT")

    app.run(host=LOCAL_HOST, port=INBOUND_PORT)