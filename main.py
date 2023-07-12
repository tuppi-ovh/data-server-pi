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

import os
import time
import sys
import importlib
import config
from telegram import TelegramClass


# constants
COMMANDS = (
    {"command": "help", "description": "Return a help message"},
    {"command": "auto", "description": "Continious reception of telegram commands"},
    {"command": "stop", "description": "Stop service execution"},
    {"command": "skip", "description": "Skip telegram messages in case of error"},
)


class MainClass:
    """ Main class.
    """

    def __init__(self):
        """ Constructor.
        """
        self.__telegram = TelegramClass()
        # plugins
        self.__list_plugins()
        self.__load_plugins()
        self.__configure_plugins(config)
        # vars
        self.__stop = False

    def __handle_plugins(self, command):
        """ Handles plugins. 
        """
        retval = []
        for plugin in self.__plugins:
            result = plugin.handle(command)
            if len(result) > 0:
                retval = result
                break
        return retval

    def __list_plugins(self):
        """ Scans for all available plugins.
        """
        self.__plugins_info = []
        possible_plugins = os.listdir(config.MAIN_PLUGINS_PATH)
        enabled_plugins = config.MAIN_PLUGINS
        if "about" in enabled_plugins:
            pass
        else:
            enabled_plugins.append("about")
        for i in possible_plugins:
            location = os.path.join(config.MAIN_PLUGINS_PATH, i)
            if (
                os.path.isdir(location)
                and ("__init__.py" in os.listdir(location))
                and (i in enabled_plugins)
            ):
                # info = imp.find_module(MainModule, [location])
                info = None
                self.__plugins_info.append({"name": i, "info": info})

    def __load_plugins(self):
        """ Loads plugins.
        """
        self.__plugins = []
        for plugin_info in self.__plugins_info:
            self.__plugins.append(
                importlib.import_module("plugins." + plugin_info["name"] + ".__init__")
            )

    def __get_commands_plugins(self):
        """ Lists plugin commands.
        """
        text = "Available commands:\n"
        for plugin in self.__plugins:
            cmds = plugin.get_commands()
            for cmd in cmds:
                text = text + "  " + cmd["command"] + "\n"
        for cmd in COMMANDS:
            text = text + "  " + cmd["command"] + "\n"
        return text

    def __configure_plugins(self, configuration):
        """ Configures plugins. 
        """
        for plugin in self.__plugins:
            plugin.configure(configuration)

    def execute_from_cgi(self, command, chat_id):
        """ Executes from CGI to be able to filter accessible commands.
        """
        retval = None
        # authorized commands (to replace by an inteligent mecanism)
        authorized_commands = [
            "about",
            "show-c",
            "show-w",
            "db.add.temper.",
            "db.add.hum.",
        ]
        for cmd in authorized_commands:
            if command.find(cmd) != -1:
                retval = self.execute(command, chat_id)
                break
        # return
        return retval

    def execute(self, command, chat_id):
        """ 
        @brief Handles a command. 
        @param command - string value of telegram command.
        @param chat_id - integer value of telegram chat ID.
        """
        retval = None

        # log
        print("[main] cmd=" + command + " chat_id=" + str(chat_id))

        # handle command in each plugin
        responses = self.__handle_plugins(command)
        if len(responses) > 0:
            for resp in responses:
                if "text" in resp:
                    self.__telegram.send_telegram_text(chat_id, resp["text"])
                if "photo" in resp:
                    self.__telegram.send_telegram_photo(chat_id, resp["photo"])
            # return value
            retval = responses
        
        # help
        elif command == "help":
            text = self.__get_commands_plugins()
            self.__telegram.send_telegram_text(chat_id, text)
            retval = [{"text": text}]

        # stop and exit
        elif command == "stop":
            text = "Stopping the service execution..."
            self.__telegram.send_telegram_text(chat_id, text)
            self.__stop = True
            retval = [{"text": text}]

        # skip telegram messages
        elif command == "skip":
            text = "Skip these commands:"
            commands = self.__telegram.recv_telegram_commands()
            for cmd in commands:
                text = text + " " + cmd["command"]
            retval = [{"text": text}]

        # recursive execution in automatic mode, not from telegram
        elif command == "auto":
            stop_last = False
            stop_last_last = False
            while not stop_last_last:
                commands = self.__telegram.recv_telegram_commands()
                for cmd in commands:
                    self.execute(cmd["command"], cmd["chat_id"])
                stop_last_last = stop_last
                stop_last = self.__stop
                time.sleep(1)

        # unknown command
        else:
            # help message
            text = '"' + command + '" is unknown command. \n'
            text = text + self.__get_commands_plugins()
            self.__telegram.send_telegram_text(chat_id, text)
            # return value
            retval = [{"text": text}]

        return retval


def main(argv):
    """ Main function.
    """
    mainc = MainClass()
    mainc.execute(argv[1], argv[2])


# Usage: python3 main.py <command> <chat_id>
# Usage example: python3 .\main.py auto -1
if __name__ == "__main__":
    main(sys.argv)
