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

import os
import time
import sys
import importlib
from base import BaseClass
from telegram import TelegramClass
from statistics import StatisticsClass
from clean import CleanClass
from mysensors import MySensorsClass
from huawei import HuaweiClass
import config


# constants
COMMANDS = ({"command": "help", "description": ""},
            {"command": "auto", "description": ""},

PLUGIN_FOLDER = "./plugins"


class MainClass(BaseClass):
    """ Main class.
    """

    def __init__(self, database):
        """ Constructor.
        """
        BaseClass.__init__(self, "main")
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
        # plugins 
        self.__list_plugins()
        self.__load_plugins()
        self.__configure_plugins(config)
        

    def __handle_plugins(self, command):
        """ Handles plugins. 
        """
        retval = None
        for plugin in self.__plugins:
            result = plugin.handle(command)
            if result != None:
                retval = result
                break
        return retval


    def __list_plugins(self):
        """ Scans for all available plugins.
        """
        self.__plugins_info = []
        possible_plugins = os.listdir(PLUGIN_FOLDER)
        enabled_plugins = (config.MAIN_PLUGINS, "about")
        for i in possible_plugins:
            location = os.path.join(PLUGIN_FOLDER, i)
            if os.path.isdir(location) and ("__init__.py" in os.listdir(location)) and (i in enabled_plugins):
                #info = imp.find_module(MainModule, [location])
                info = None
                self.__plugins_info.append({"name": i, "info": info})


    def __load_plugins(self):
        """ Loads plugins.
        """
        self.__plugins = []
        for plugin_info in self.__plugins_info:
            self.__plugins.append(importlib.import_module("plugins." + plugin_info["name"] + ".__init__"))

    
    def __get_commands_plugins(self):
        """ Lists plugin commands.
        """
        text = "Available commands:\n"
        for plugin in self.__plugins:
            cmds = plugin.get_commands()
            for c in cmds:
                text = text + "  " + c["command"] + "\n"
        for c in COMMANDS:
            text = text + "  " + c["command"] + "\n"
        return text


    def __configure_plugins(self, config):
        """ Configures plugins. 
        """
        for plugin in self.__plugins:
            plugin.configure(config)


    def execute(self, argv):
        """ Executes once.
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

            # handle command in each plugin
            responses = self.__handle_plugins(command)
            if len(responses) > 0:
                for r in responses:
                    if "text" in r:
                        self.__telegram.send_telegram_text(chat_id, r["text"])
                    if "photo" in r:
                        self.__telegram.send_telegram_photo(chat_id, r["photo"])

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

            # help
            elif command == "help":
                text = self.__get_commands_plugins()
                self.__telegram.send_telegram_text(chat_id, text)

            # for internal use, not from telegram
            elif command == "mysensors-dont-call-from-telegram":
                self.__mysensors.run()

            # recursive execution in automatic mode, not from telegram
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
                # help message
                text = "\"" + command + "\" is unknown command. \n"
                text = text + self.__get_commands_plugins()
                self.__telegram.send_telegram_text(chat_id, text)
                # log
                self.log_error(text)

        else:
            self.log_error("incorrect number of args")


def main(argv):
    """ Main function.
    """
    mainc = MainClass(argv[1])
    mainc.execute(argv)


# Usage: python3 main.py <database> <command> <chat_id>
# Usage example: python3 .\main.py .\MySensors.db auto -1
if __name__ == "__main__":
    main(sys.argv)
