# 슬랙과 연동하여 DB를 갱신하거나, 조회하는 업무를 수행하는 서비스
import os
from dotenv import load_dotenv
load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("BOT_USER_TOKEN")

from slack_sdk.rtm import RTMClient

from utils.slack import SlackStockBot

@RTMClient.run_on(event="message")
def listen_message(**payload):
    text = payload['data']["text"]
    channel_id = payload["data"]["channel"]
    user = payload["data"]["user"]
    web_client = payload['web_client']

    slack_bot = SlackStockBot()

    result = slack_bot.main(user, text)
    web_client.chat_postMessage(channel=channel_id, text=result)

rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
rtm_client.start()