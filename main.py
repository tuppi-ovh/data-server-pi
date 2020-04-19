"""
Data Server PI - high level application for the Smart Home data acquisition.
Copyright (C) 2020 Vadim MUKHTAROV

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

import time
import sys
from base import BaseClass
from telegram import TelegramClass
from statistics import StatisticsClass
from clean import CleanClass
from mysensors import MySensorsClass
from meteo import MeteoClass
from huawei import HuaweiClass



class MainClass(BaseClass):
    """
    brief: Main class.

    Available methods: 
    - execute the command parse
    """

    def __init__(self, database):
        """
        Constructor.
        """
        BaseClass.__init__(self, "main")
        self.__meteo = MeteoClass("meteo")
        self.__telegram = TelegramClass("telegram")
        self.__huawei = HuaweiClass("huawei")
        if database != None:
            self.__statistics = StatisticsClass("statistics", database)
            self.__clean = CleanClass("clean", database)
            self.__mysensors = MySensorsClass("mysensors", database)
        else:
            self.__statistics = None
            self.__clean = None
            self.__mysensors = None
        

    def execute(self, argv):
        """
        Execute once.
        """

        if len(argv) == 4:

            # convert sys argv to normal variables
            filename = argv[0]
            db_filename = argv[1]
            command = argv[2]
            chat_id = int(argv[3])

            # log
            self.log_info("len=" + str(len(argv)) + " file=" + filename +
                        " db=" + db_filename + " cmd=" + command + " chat=" + str(chat_id))

            # meteo for today 
            if command == "meteo":
                message = self.__meteo.get_meteo(0)
                print("meteo: ", message)
                self.__telegram.send_telegram_text(chat_id, message)

            # meteo for tomorrow
            elif command == "meteo.demain":
                message = self.__meteo.get_meteo(1)
                self.__telegram.send_telegram_text(chat_id, message)

            # meteo for after tomorrow
            elif command == "meteo.demain.apres":
                message = self.__meteo.get_meteo(2)
                self.__telegram.send_telegram_text(chat_id, message)

            # data usage statistics
            elif command == "huawei":
                message = self.__huawei.get_usage_gbytes()
                self.__telegram.send_telegram_text(chat_id, message)

            # automatic clean of MySensors database
            elif command == "clean":
                self.__clean.clean_auto()
                self.__telegram.send_telegram_text(chat_id, "Les stats ont été netoyés")

            # clean MySensors database by the entry ID
            elif command.find("clean.id.") != -1:
                try:
                    __, ___, ident = command.split(".")
                    clean.clean_by_id(int(ident))
                    telegram.send_telegram_text(chat_id, "Element supprimé : " + ident)
                except:
                    self.__telegram.send_telegram_text(chat_id, "Erreur du parsing")

            # Temperature & Humidity Statistics
            elif command.find("stats.") != -1:
                try:
                    __, temp_hum, duration = command.split(".")
                    if temp_hum == "temper":
                        filename = self.__statistics.update_temperature(duration)
                    else:
                        filename = self.__statistics.update_humidity(duration)
                    self.__telegram.send_telegram_photo(chat_id, filename)
                except:
                    self.__telegram.send_telegram_text(chat_id, "Erreur du parsing")

            # kisses for your Mississ
            elif command == "bisous":
                self.__telegram.send_telegram_text(chat_id, r":\* :\* :\*")

            # test message
            elif command == "test":
                self.__telegram.send_telegram_text(chat_id, "La commande test a été bien reçue")

            # not supported yet 
            elif command == "local":
                self.__telegram.send_telegram_text(chat_id, "La commande arrive bientôt")

            # for internal use, not from telegram
            elif command == "mysensors-dont-call-from-telegram":
                self.__mysensors.run()

            # about program
            elif command == "about":
                text = (
                    "Data Server PI - Copyright (C) 2020 - Vadim MUKHTAROV\n"
                    "This program comes with ABSOLUTELY NO WARRANTY; for details send the command 'show-w'. "
                    "This is free software, and you are welcome to redistribute it "
                    "under certain conditions; send the command 'show-c' for details."
                )
                self.__telegram.send_telegram_text(chat_id, text)

            # licence warranty
            elif command == "show-w":
                text = (
                    "This program is distributed in the hope that it will be useful, "
                    "but WITHOUT ANY WARRANTY; without even the implied warranty of "
                    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
                    "GNU General Public License for more details."
                )
                self.__telegram.send_telegram_text(chat_id, text)

            # licence redistribute
            elif command == "show-c":
                text = (
                    " This program is free software: you can redistribute it and/or modify "
                    "it under the terms of the GNU General Public License as published by "
                    "the Free Software Foundation, either version 3 of the License, or "
                    "(at your option) any later version."
                )
                self.__telegram.send_telegram_text(chat_id, text)

            # recursive execution in automatic mode
            elif command == "auto":
                while True:
                    commands = self.__telegram.recv_telegram_commands()
                    for cmd in commands:
                        argv[2] = cmd["command"]
                        argv[3] = str(cmd["chat_id"])
                        self.execute(argv)
                    time.sleep(1)

            # unknown command
            else:
                self.log_error("unknown command")
                # help message
                message = ""
                message = message + "Liste des commandes disponibles :\n"
                message = message + "  meteo\n"
                message = message + "  meteo.demain\n"
                message = message + "  meteo.demain.apres\n"
                message = message + "  bisous\n"
                message = message + "  test\n"
                message = message + "  stats.temper.<duration>\n"
                message = message + "  stats.hum.<duration>\n"
                message = message + "  clean\n"
                message = message + "  clean.id.<num>\n"
                message = message + "  about\n"
                message = message + "  show-w\n"
                message = message + "  show-c\n"
                self.__telegram.send_telegram_text(chat_id, message)

        else:
            self.log_error("incorrect number of args")


def main(argv):
    """
    Main function.
    """
    mainc = MainClass(argv[1])
    mainc.execute(argv)


# Usage: python3 main.py <database> <command> <chat_id>
# Usage example: python3 .\github\data-server-pi\main.py .\MySensors.db auto -1  
if __name__ == "__main__":
    main(sys.argv)
