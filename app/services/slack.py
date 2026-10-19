import os

import requests
from flask import current_app

SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


def send_slack_notification(message):
    """post a message to the configured Slack channel"""
    token = os.environ.get("SLACK_BOT_TOKEN")

    try:
        response = requests.post(
            SLACK_POST_MESSAGE_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "channel": os.environ.get("SLACK_CHANNEL"),
                "text": message,
            },
            timeout=5,
        )
        slack_response = response.json()
        if not slack_response.get("ok"):
            current_app.logger.warning(
                f"Slack notification failed: {slack_response.get('error')}"
            )
    except requests.RequestException as error:
        current_app.logger.warning(f"Failed to send Slack notification: {error}")
