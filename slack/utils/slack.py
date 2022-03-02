from datetime import datetime

import yfinance as yf

from utils import db

class SlackStockBot:
    """
        slack에서 메시지를 분석하여 주식정보를 제공
    """
    def __init__(self):
        pass

    def show_command_examples(self):
        """
            사용할 수 있는 명령어의 예시를 제공
        """
        result = "[COMMAND LIST]\n" 
        result += "- HELP : show command examples\n"
        result += "- SHOW TICKERS: show all saving tickers\n"
        result += "- INSERT TICKER {TICKER_NAME}: insert ticker in db\n"
        result += "- DELETE TICKER {TICKER_NAME}: delete ticker in db\n"
        result += "- SUMMARY : summary stock's indexs"

        return result

    def get_stock_tickers(self):
        """
            DB에 저장된 ticker들 반환
        """
        conn = db.get_connector()
        cur = conn.cursor()

        sql = "SELECT * FROM service.tb_ticker"

        cur.execute(sql)
        tickers = list(map(lambda x:x[0], cur.fetchall()))

        cur.close()
        conn.close()

        return tickers

    def show_stock_tickers(self,):
        """
            DB에 저장된 ticker 목록을 제공
        """
        tickers = self.get_stock_tickers()
        return "[TICKER LIST]\n" + ", ".join(tickers)

    def insert_ticker(self, ticker):
        """
            DB에 ticker를 추가
        """
        # check valid ticker
        _ticker = yf.Ticker(ticker)
        if not hasattr(_ticker, "info") or not _ticker.info["marketCap"]:
            return f"[ERROR] {ticker} is invalid ticker name"

        self.delete_ticker(ticker) # 중복 제거

        conn = db.get_connector()
        cur = conn.cursor()
        
        sql = f"""
            INSERT INTO service.tb_ticker (ticker)
            VALUES ('{ticker}')
        """

        cur.execute(sql)
        cur.close()
        conn.close()

        return f"AFTER {self.show_stock_tickers()}"

    def show_summary(self):
        """
            요약 테이블에 포함된 정보들을 반환
        """
        result = "[RECENT MDD LIST]\n"

        tickers = self.get_stock_tickers()
        conn = db.get_connector()
        cur = conn.cursor()

        for ticker in tickers:
            sql = f"""
                SELECT ts, adj_close, mv200, high_52w, low_52w FROM summary.stock
                WHERE ticker='{ticker}'
                ORDER BY ts DESC
                LIMIT 2
            """
            cur.execute(sql)

            result += f"\t{ticker}\n"
            for (ts, adj_close, mv200, high_52w, low_52w) in cur.fetchall():
                result += f"\t\t{datetime.strftime(ts, '%Y-%m-%d')}"
                result += f"\tadj_close: {adj_close:.2f}$" 
                result += f"\tmv200: {mv200:.2f}$"
                result += f"\thigh_52w: {-high_52w:.2f}%"
                result += f"\tlow_52w: {low_52w:.2f}%\n"

        cur.close()
        conn.close()

        return result

    def delete_ticker(self, ticker):
        """
            DB에 저장된 ticker를 제거 후 남은 목록 확인
        """
        conn = db.get_connector()
        cur = conn.cursor()

        sql = f"""
            DELETE FROM service.tb_ticker
            WHERE ticker = '{ticker}'
        """
        cur.execute(sql)

        cur.close()
        conn.close()

        return f"AFTER {self.show_stock_tickers()}"

    def main(self, user_name, text):
        """
            메시지를 분석하여 옳바른 반응을 제공
        """
        text = text.upper()
        result = f"<@{user_name}>\n"

        # show tickers
        if text.startswith("SHOW") and "TICKER" in text:
            result += self.get_stock_tickers()
        # insert ticker
        elif text.startswith("INSERT") and "TICKER" in text:
            ticker = text.split()[-1].strip()
            result += self.insert_ticker(ticker)
        # delete ticker
        elif text.startswith("DELETE") and "TICKER" in text:
            ticker = text.split()[-1].strip()
            result += self.delete_ticker(ticker)
        # show stock's summary
        elif text.startswith("SUMMARY"):
            result += self.show_summary()

        else: # default
            result += self.show_command_examples()

        return result
