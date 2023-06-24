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

# For more API calls just look on code in the huawei_lte_api/api folder, there is no separate DOC yet

import sys
import collections
from datetime import datetime 
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection


# constants
COMMANDS = [
    {"command": "huawei.usage", "description": ""},
    {"command": "huawei.quota", "description": ""},
    {"command": "huawei.test", "description": ""}
]

# config
config_url = None
config_count_day = None
config_count_limit = 100


def __get_usage_gbytes():
    """
    """
    try:
        connection = AuthorizedConnection(config_url)
        stats = connection.get("monitoring/month_statistics")
        usage = (
            (int(stats["CurrentMonthDownload"]) + int(stats["CurrentMonthUpload"]))
            / 1024
            / 1024
            / 1024
        )
        return "{:.2f} GB".format(usage)
    except:
        return "no access"

def __get_quota_gbytes():
    """
    """
    try:
        connection = AuthorizedConnection(config_url)
        stats = connection.get("monitoring/month_statistics")
        usage = (
            (int(stats["CurrentMonthDownload"]) + int(stats["CurrentMonthUpload"]))
            / 1024
            / 1024
            / 1024
        )
        print(stats)
        # dates
        now = datetime.now()
        end = now
        end = end.replace(day = config_count_day)
        end = end.replace(hour = 0)
        end = end.replace(minute = 0)
        if now.day > end.day:
            if now.month == 12:
                end = end.replace(month = 1)
                end = end.replace(year = now.year + 1)
            else:
                end = end.replace(month = now.month + 1)
        # quota
        diff = datetime.timestamp(end) - datetime.timestamp(now)
        quota = (config_count_limit - usage) / diff * 3600 * 24
        return "{:.2f} GB/day".format(quota)
    except:
        return "no access"

def __test():
    """
    """
    retval = ""
    with Connection(config_url) as connection:
        client = Client(connection) 
        # signal
        retval = str(client.device.signal())
        # info
        retval = retval + "\n" + str(client.device.information()) 
        # wifi info
        retval = retval + "\n" + str(connection.get("wlan/basic-settings"))
        retval = retval + "\n" + str(client.wlan.basic_settings())
        retval = retval + "\n" + str(connection.post_set('wlan/basic-settings', collections.OrderedDict((
            ('WifiEnable', 1),
            ('WifiHide', 0)
        ))))
    return retval

def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # internet usage
    if command == "huawei.usage":
        text = __get_usage_gbytes()
        retval.append({"text": text})
    # daily quota
    elif command == "huawei.quota":
        text = __get_quota_gbytes()
        retval.append({"text": text})
    # test
    elif command == "huawei.test":
        text = __test()
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
    global config_count_day
    global config_count_limit

    config_url = config.HUAWEI_URL
    config_count_day = config.HUAWEI_COUNT_DAY
    config_count_limit = config.HUAWEI_COUNT_LIMIT

def main(argv):
    """ Main function."""
    # config
    config = collections.namedtuple("config", ["HUAWEI_URL", "HUAWEI_COUNT_DAY", "HUAWEI_COUNT_LIMIT"])
    config.HUAWEI_URL = argv[2]
    config.HUAWEI_COUNT_DAY = int(argv[3])
    config.HUAWEI_COUNT_LIMIT = int(argv[4])
    configure(config)
    # handle
    msg = handle(argv[1])
    # print
    if len(msg) > 0:
        print(msg[0]["text"])


# Usage example: python3 plugins/huawei/__init__.py huawei.usage http://admin:admin@192.168.8.1/ 1 100
if __name__ == "__main__":
    main(sys.argv)
