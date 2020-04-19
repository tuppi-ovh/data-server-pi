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

import platform
import config
from datetime import datetime


class BaseClass(object):
    """Base class for all modules."""

    def __init__(self, name):
        self.__name = name

    def log_info(self, message):
        self.__log("INFO", message)

    def log_error(self, message):
        self.__log("ERROR", message)

    def __log(self, type_str, message):
        msg = "[" + str(datetime.now()) + "][" + type_str + \
            "][" + self.__name + "] " + message
        if config.BASE_LOG_FILE_ENABLED:
            with open(config.BASE_LOG_FILENAME, 'ab') as f:
                f.write((msg + "\n").encode('utf8'))
        print(msg)


def main():
    """ Main function to test the module."""
    # handler object
    base = BaseClass("base")
    # log message
    base.log_info("hello world!")


# Usage: python3 base.py
if __name__ == "__main__":
    main()
