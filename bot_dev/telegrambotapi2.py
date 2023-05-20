from typing import Any
import requests
import json

token = ""

######################################################## 1


def getMe() -> None:
    """for test bot only"""
    method = "getMe"
    url = f"https://api.telegram.org/bot{token}/{method}"
    with requests.get(url) as response:
        print(json.dumps(json.loads(response.text), indent=2))


# getMe()

######################################################## 2


def getUpdates(url: str) -> dict[str, Any]:
    """to check updates. result list will be not empty after /start bot"""
    # method = "getUpdates"
    with requests.get(url) as response:
        return response.json()


# getUpdates()


######################################################## 3


def sendMessage(chat_id: str, text: str, token: str) -> dict[str, Any]:
    """to send mesage to user"""
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{token}/{method}"
    params = {"chat_id": chat_id, "text": text}
    with requests.get(url, params=params) as response:
        return response.json()


# sendMessage()
