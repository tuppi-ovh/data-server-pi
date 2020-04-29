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

# For more API calls just look on code in the huawei_lte_api/api folder, there is no separate DOC yet

import sys
import collections
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection


# constants
COMMANDS = [{"command": "huawei", "description": ""}]

# config
config_url = None



def __get_usage_gbytes():
    """
    """
    try:
        connection = AuthorizedConnection(config_url)
        stats = connection.get('monitoring/month_statistics')
        usage = (int(stats["CurrentMonthDownload"]) + int(stats["CurrentMonthUpload"])) / 1024 / 1024 / 1024
        return "{:.2f} GB".format(usage)
    except:
        return "no access"


def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # internet usage
    if command == "huawei":
        text = __get_usage_gbytes()
        retval.append({"text": text})
    # other commands
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
    global config_url
    config_url = config.HUAWEI_URL


def main(argv):
    """ Main function."""
    # config
    config = collections.namedtuple('config', ['HUAWEI_URL'])
    config.HUAWEI_URL = argv[2]
    configure(config)
    # handle
    msg = handle(argv[1])
    # print 
    if len(msg) > 0:
        print(msg[0]["text"])


# Usage: python3 __init__.py <command> 
# Usage example: python3 .\plugins\huawei\__init__.py huawei http://admin:admin@192.168.8.1/
if __name__ == "__main__":
    main(sys.argv)

