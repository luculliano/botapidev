"""echo bot"""
import os
import time

from telegrambotapi2 import getUpdates, sendMessage

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if token is None:
        exit()
    counter = 1
    offset = -2
    while counter <= 20:
        # as the first offset will be -1, bellow a get the value
        # and increase it + 1 too
        updates = getUpdates(
            f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
        )
        print("query for updates", counter)
        if updates["result"]:
            offset = updates["result"][0]["update_id"]
            chat_id = updates["result"][0]["message"]["from"]["id"]
            name = updates["result"][0]["message"]["from"]["username"]
            print("replying...")
            sendMessage(chat_id, f"Hello, {name}!", token)
        # get query to server for getUpdates each second
        time.sleep(1)
        counter += 1
