# -*- coding: utf-8 -*-
# it is required for french characters

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

import sys
import requests
import collections
from bs4 import BeautifulSoup
from daemon import MySensorsClass


# constants
COMMANDS = ({"command": "mysensors-dont-call-from-telegram", "description": ""})


# config
config_database = None
config_serial_port = None


def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # meteo for today 
    if command == "mysensors-dont-call-from-telegram":
        mysensors = MySensorsClass(config_serial_port, config_database)
        mysensors.run() # stay here forever
    # unknown command
    else:
        pass
    # return 
    return retval


def get_commands():
    """ Returns a list of all supporteed commands.
    """
    return COMMANDS


def configure(config):
    """ Configures the plugin regarding configuration file.
    """
    global config_database
    global config_serial_port
    config_database = config.MYSENSORS_DATABASE_FILENAME
    config_serial_port = config.MYSENSORS_SERIAL_PORT

def main(argv):
    """ Main function."""
    # config
    config = collections.namedtuple('config', ['MYSENSORS_DATABASE_FILENAME', 'MYSENSORS_SERIAL_PORT'])
    config.MYSENSORS_DATABASE_FILENAME = argv[2]
    if argv[3] == "None":
        config.MYSENSORS_SERIAL_PORT = None
    else:
        config.MYSENSORS_SERIAL_PORT = argv[3]
    configure(config)
    # handle
    msg = handle(argv[1])
    # print 
    if len(msg) > 0:
        print(msg[0]["text"])


# Usage: python3 __init__.py <command> <database> <serial_port>
# Usage example: python3 .\plugins\mysensors_daemon\__init__.py mysensors-dont-call-from-telegram .\MySensors.db None
if __name__ == "__main__":
    main(sys.argv)
