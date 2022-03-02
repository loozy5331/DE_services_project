import os

import requests
from dotenv import load_dotenv

if __name__=="__main__":
    load_dotenv()
    PORT  = os.environ.get("INBOUND_PORT")

    url = f"http://localhost:{PORT}/service/stock"
    print(url)

    res = requests.post(url)

    print(f"status:{res.status_code}, text:{res.text}")