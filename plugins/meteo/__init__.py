# -*- coding: utf-8 -*-
# it is required for french characters

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
import requests
import collections
from bs4 import BeautifulSoup


# constants
COMMANDS = [
    {"command": "meteo", "description": ""},
    {"command": "meteo.demain", "description": ""},
    {"command": "meteo.demain.apres", "description": ""},
]

# config
config_url = None


def __get_meteo(day):
    """ Parses the meteo site to get interesting information.
    """
    # get pages
    r_15d = requests.get(config_url)

    # parse
    soup_15d = BeautifulSoup(r_15d.text, features="html.parser")

    # defaults
    rain = "NA"
    rain_mm = "NA"
    temper_morning = "NA"
    temper_evening = "NA"
    wind = "NA"
    last_update = "NA"

    ##### Last Update #####
    # parse soup
    last_update_raw = soup_15d.find("div", attrs={"class": u"small"}).text
    # format
    last_update_split = last_update_raw.split("\n")
    last_update = (
        last_update_split[1].replace("Dernière mise à jour : ", "").replace("  ", "")
    )

    ##### Rain #####
    # parse soup
    rain = soup_15d.find_all(
        "span", attrs={"class": u"forecast-line__additionnal--rain-proba"}
    )[day].text
    # format
    rain = rain.replace("\n", "").replace(" ", "")

    ##### Rain in mm #####
    # parse soup
    rain_mm = soup_15d.find_all(
        "div", attrs={"class": u"forecast-line__additionnal-mobile--rain-quantity"}
    )[day].text
    # format
    rain_mm = rain_mm.replace("\n", "").replace(" ", "").replace("pluie24h:", "")

    ##### Temperature #####
    # parse soup
    temper_morning = soup_15d.find_all(
        "div", attrs={"class": u"forecast-line__pictos--temp"}
    )[day * 2].text
    temper_evening = soup_15d.find_all(
        "div", attrs={"class": u"forecast-line__pictos--temp"}
    )[day * 2 + 1].text

    ##### Wind #####
    # parse soup
    wind = soup_15d.find_all(
        "div", attrs={"class": u"forecast-line__additionnal-mobile--wind--direction"}
    )[day].text
    # format
    wind = wind.replace("\n", " ").replace("  ", "").replace("km/h ", "km/h")

    ##### Output #####
    # output
    output = ""
    output = output + "Pluie: " + rain + " (" + rain_mm + "). \n"
    output = (
        output + "Température: " + temper_morning + " - " + temper_evening + " °C. \n"
    )
    output = output + "Vent: " + wind + ". \n"
    output = output + "Màj: " + last_update + ". "
    # format
    output = output.replace("  ", " ")
    return output

def handle(command):
    """ Handles telegram command.
    """
    retval = []
    # meteo for today
    if command == "meteo":
        retval.append({"text": __get_meteo(0)})
    # meteo for tomorrow
    elif command == "meteo.demain":
        retval.append({"text": __get_meteo(1)})
    # meteo for after tomorrow
    elif command == "meteo.demain.apres":
        retval.append({"text": __get_meteo(2)})
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
    global config_url
    config_url = config.METEO_URL

def main(argv):
    """ Main function."""
    # config
    config = collections.namedtuple("config", ["METEO_URL"])
    config.METEO_URL = argv[2]
    configure(config)
    # handle
    msg = handle(argv[1])
    # print
    if len(msg) > 0:
        print(msg[0]["text"])

# Usage: python3 __init__.py <command> <config_url>
# Usage example: python3 .\plugins\meteo\__init__.py meteo.demain <config_url>
if __name__ == "__main__":
    main(sys.argv)
