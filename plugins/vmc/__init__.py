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
COMMANDS = [{"command": "vmc.set.<high>.<low>.<hyst>", "description": ""}]

# config
config_www = None


def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # about program
    if command.find("vmc.set.") != -1:
        __, ___, high, low, hyst = command.split(".")
        with open(os.path.join(config_www, "cmd_vmc.txt"), "w") as f:
            high_i = int(high)
            low_i = int(low)
            hyst_i = int(hyst)
            f.write("%d,%d,%d,%d" % (high_i, low_i, hyst_i, high_i + low_i + hyst_i))
        text = "done"
        retval.append({"text": text})
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
    global config_www
    config_www = config.VMC_WWW_PATH
