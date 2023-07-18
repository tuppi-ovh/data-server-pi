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
import sys


# constants
COMMANDS = [{"command": "echo.<message.with.points>", "description": ""}]


def handle(command):
    """ Handles echo command.
    """
    retval = []
    # about program
    if command.find("echo.") != -1:
        text = command[5:len(command)]
        retval.append({"text": text})
    # unknown command
    else:
        pass
    # return
    return retval

def handle_bgnd():
    """ Bgnd task.
    """
    retval = []
    return retval

def get_commands():
    """ Returns a list of all supporteed commands.
    """
    return COMMANDS

def configure(config):
    """ Configures the plugin regarding configuration file.
    """
    # pylint: disable=W0613
    return