"""
Data Server PI - high level application for the Smart Home data acquisition.
Copyright (C) 2020-2023 tuppi-ovh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For information on Data Server PI: tuppi.ovh@gmail.com
"""

import sys
import json
import requests
import config

TIMEOUT_TELEGRAM = 60 * 2
TIMEOUT_REQUESTS = TIMEOUT_TELEGRAM + 30


URL = "https://api.telegram.org/bot" + config.TELEGRAM_BOT_TOKEN


class TelegramClass:
    def __init__(self):
        self.__updates_offset = 0
        self.__counter_send = 0

    def send_telegram_text(self, chatid, message):
        """ Send text message to destination.
        """
        data = {"chat_id": str(chatid), "text": message}
        if chatid != -1:
            __ = requests.get(URL + "/sendMessage", params=data)
        # log
        print("[telegram] text: " + message)

    def send_telegram_photo(self, chatid, filename):
        """ Send a photo to destination.
        """
        data = {"chat_id": str(chatid)}
        files = {"photo": open(filename, "rb")}
        if chatid != -1:
            __ = requests.get(URL + "/sendPhoto", params=data, files=files)
        # log
        print("[telegram] photo: " + filename)

    def recv_telegram_commands(self):
        """
        For more information visit: 
        https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
        """
        commands = []

        # url
        url_custom = (
            URL
            + "/getUpdates?timeout="
            + str(TIMEOUT_TELEGRAM)
            + "&offset="
            + str(self.__updates_offset)
        )
        # log for debug
        print("url=" + url_custom)

        # url request
        try:
            response = requests.get(url_custom, timeout=TIMEOUT_REQUESTS)
            # log for debug
            print("requests get ok (status_code=" + str(response.status_code) + ")")

        # exceptions
        except requests.exceptions.Timeout as error:
            print("requests get exception: " + str(error))
        except:
            print("requests get exception")

        # continue if succeeded
        else:
            if response.status_code == 200:
                # json
                updates = json.loads(response.content.decode("utf8"))
                # log for debug
                print("json ok")
                print(
                    "offset="
                    + str(self.__updates_offset)
                    + " updates_nb="
                    + str(len(updates["result"]))
                )
                # handle updates
                if updates["ok"] and len(updates["result"]) > 0:

                    # calculate update offset
                    update_ids = []
                    for update in updates["result"]:
                        update_ids.append(int(update["update_id"]))
                    self.__updates_offset = max(update_ids) + 1
                    # debug: print("New offset: " + str(updates_offset))

                    # commands
                    for update in updates["result"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"].lower()
                        # debug: print("chat_id: " + str(chat_id))
                        if chat_id in config.TELEGRAM_CHAT_ID_LIST:
                            command = {}
                            command["chat_id"] = chat_id
                            command["command"] = text
                            commands.append(command)
                            # log
                            print("recv command=" + text + " chatid=" + str(chat_id))

        return commands


def main(argv):
    """ Main function."""

    # handler object
    telegram = TelegramClass()

    chat_id = int(argv[1])
    function = argv[2]
    parameter = argv[3]

    if function == "send_telegram_text":
        telegram.send_telegram_text(chat_id, parameter)
    elif function == "send_telegram_photo":
        telegram.send_telegram_photo(chat_id, parameter)


# Standalone execution: python3 telegram.py <chat_id> <function> <parameter>
# Example: python3 .\github\data-server-pi\telegram.py 873550202 send_telegram_text hello!
if __name__ == "__main__":
    main(sys.argv)
