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

import sys


# constants
COMMANDS = [
    {"command": "about", "description": ""},
    {"command": "show-w", "description": ""},
    {"command": "show-c", "description": ""},
]


def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # about program
    if command == "about":
        text = (
            "Data Server PI - Copyright (C) 2020-2023 tuppi-ovh\n"
            "This program comes with ABSOLUTELY NO WARRANTY; for details send the command 'show-w'. "
            "This is free software, and you are welcome to redistribute it "
            "under certain conditions; send the command 'show-c' for details."
        )
        retval.append({"text": text})
    # licence warranty
    elif command == "show-w":
        text = (
            "This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
            "GNU General Public License for more details."
        )
        retval.append({"text": text})
    # licence redistribute
    elif command == "show-c":
        text = (
            " This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version."
        )
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

def main(argv):
    """ Main function."""
    # config
    config = None
    configure(config)
    # handle
    msg = handle(argv[1])
    # print
    if len(msg) > 0:
        print(msg[0]["text"])

# Usage: python3 __init__.py <command>
# Usage example: python3 .\plugins\about\__init__.py about
if __name__ == "__main__":
    main(sys.argv)
