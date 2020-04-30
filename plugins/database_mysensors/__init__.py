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
from .mysensors import MySensorsClass
from .clean import CleanClass
from .statistics import StatisticsClass


# constants
COMMANDS = [
    {"command": "mysensors-dont-call-from-telegram", "description": ""},
    {"command": "db.clean.auto", "description": ""},
    {"command": "db.clean.id.<id>", "description": ""},
    {"command": "db.stat.temper.<duration>", "description": ""},
    {"command": "db.stat.hum.<duration>", "description": ""},
    {"command": "db.add.temper.<node_id>.<child_sensor_id>.<temper>", "description": ""},
    {"command": "db.add.hum.<node_id>.<child_sensor_id>.<hum>", "description": ""}
]



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

    # automatic clean of MySensors database
    elif command == "db.clean.auto":
        clean = CleanClass(config_database)
        clean.clean_auto()
        text = "done"
        retval.append({"text": text})

    # clean MySensors database by the entry ID
    elif command.find("db.clean.id.") != -1:
        __, ___, ident = command.split(".")
        clean = CleanClass(config_database)
        clean.clean_by_id(int(ident))
        text = "Element ID=" + ident + " is deleted"
        retval.append({"text": text})

    # Temperature Statistics
    elif command.find("db.stat.temper") != -1:
        __, ___, duration = command.split(".")
        statistics = StatisticsClass(config_database)
        filename = statistics.update_temperature(duration)
        retval.append({"photo": filename})

    # Humidity Statistics
    elif command.find("db.stat.hum") != -1:
        __, ___, duration = command.split(".")
        statistics = StatisticsClass(config_database)
        filename = statistics.update_humidity(duration)
        retval.append({"photo": filename})

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
    """ Main function for standalone execution.
    """
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
