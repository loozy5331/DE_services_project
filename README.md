# DE_services_project
DE_workflow_project에서 활용할 소스 데이터들을 수집하는 API 서비스 모음

### service-stock.py
 주식 정보를 불러와서 DB에 저장하는 서비스. 

* 동작 개요
    1. POST method로 json에 담아서 tickers를 전달 (ex. json={"tickers":\["SPY"\]})
    2. yfinance 라이브러리를 통해 주식 정보 추출
    3. 연결된 DB에 테이블 생성 및 데이터 추가 후 종료
        - ts(timestamp): 주가 측정일
        - close(FLOAT): 종가
        - ticker(VARCHAR): 주식의 고유명사(?)


* 사전 조건
 - postgreSQL14 설치 및 실행
 - requirements.txt 파일 설치
 - .env 파일 생성
<pre><code># ".env" 파일 
# 환경변수 목록

# global
LOCAL_HOST = "{LOCAL IP ADDRESS}" # (ex. "192.168.45.7")

# api(flask)
INBOUND_PORT = "{PORT}" # (ex. "50003")

# db(postgreSQL)
DB_USER_NAME = "{postgreSQL user ID}" # (ex. "postgres")
DB_PASSWORD = "{postgreSQL user password}" # (ex. "postgres")
DB_PORT = "{postgreSQL PORT}" # (ex. "5432")
</code></pre>
