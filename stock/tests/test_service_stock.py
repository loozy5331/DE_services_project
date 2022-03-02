import os

import requests
from dotenv import load_dotenv

if __name__=="__main__":
    load_dotenv()
    LOCAL_HOST = os.environ.get("LOCAL_HOST")
    PORT  = os.environ.get("INBOUND_PORT")

    url = f"http://{LOCAL_HOST}:{PORT}/service/stock"

    res = requests.post(url, json={"tickers":["QQQ", "SPY"]})
    print(res.text)