# 슬랙과 연동하여 DB를 갱신하거나, 조회하는 업무를 수행하는 서비스
import os
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("BOT_USER_TOKEN")

from slack import RTMClient
import requests

@RTMClient.run_on(event="message")
def amusebot(**payload):
    """
    This function triggers when someone sends
    a message on the slack
    """
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")

    # If a message is not send by the bot
    if bot_id == "":
        channel_id = data["channel"]

        # Extracting message send by the user on the slack
        text = data.get("text", "")
        text = text.split(">")[-1].strip()

        response = ""
        if "help" in text.lower():
            user = data.get("user", "")
            response = f"Hi <@{user}>! I am AmuseBot :)"
        else:
            activity_json_response = requests.get("http://www.boredapi.com/api/activity/").json()
            activity = activity_json_response['activity']
            response = str(activity)
        
        # Sending message back to slack
        web_client.chat_postMessage(channel=channel_id, text=response)

try:
    rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
    print("Bot is up and running!")
    rtm_client.start()
except Exception as err:
    print(err)
