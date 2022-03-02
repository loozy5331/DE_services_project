<h1> DE_services_project </h1>

<h2> 목표 </h2>

DE_workflow_project에서 활용할 소스 데이터들을 수집하는 API 서비스 모음

![etl_pipeline-services drawio](https://user-images.githubusercontent.com/36221276/156317538-e2da3a4c-3acc-4972-ae29-99b2952e0ba9.png)

<h2> 서비스 목록 </h2>
<h3> stock </h3>
 
 저장된 주식 목록의 주가 정보를 DB에 저장하는 서비스. 

<h3> slack </h3>

 slack의 RTM(Real Time Messaging) bot 기능을 통해 아래의 기능들을 수행
 1. 수집할 ticker(주식의 ID) 추가 및 삭제
 2. 요약 테이블 정보 출력
 3. 현재 수집 중인 ticker 확인


<h2> 사전 조건 </h2>

1. OLTP(DB) 설치(현재 postgreSQL14)
2. docker-compose를 통해 서비스들 실행

<h2> 코드 변경 시 유의사항</h2>
1. DB 변경을 위해서는 각 서비스 폴더에 .env 파일을 생성해주어야 함.

```text
# ".env" 파일 
# DB 환경변수 목록

# db(postgreSQL)
DB_HOST = "{YOUR DB HOST}"    # ex. 192.168.0.1
DB_USER_NAME = "{DB USER}"    # ex. postgres
DB_PASSWORD = "{DB PASSWORD}" # ex. postgres
DB_PORT = "{DB PORT}"         # ex. 5432
```
