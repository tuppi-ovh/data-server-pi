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
from bs4 import BeautifulSoup
from base import BaseClass
import config


class MeteoClass(BaseClass):
    """
    """

    def __init__(self, name):
        """
        Constructor.
        """
        BaseClass.__init__(self, name)
        self.__counter_meteo = 0

    def get_meteo(self, day):
        """
        Parse the meteo site to get interesting information.
        """
        self.__counter_meteo = self.__counter_meteo + 1

        # get pages
        r_15d = requests.get(config.METEO_URL)

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
        last_update = last_update_split[1].replace("Dernière mise à jour : ", "").replace("  ", "")

        ##### Rain #####
        # parse soup
        rain = soup_15d.find_all(
            "span", attrs={"class": u"forecast-line__additionnal--rain-proba"})[day].text
        # format 
        rain = rain.replace("\n", "").replace(" ", "")

        ##### Rain in mm #####
        # parse soup
        rain_mm = soup_15d.find_all(
            "div", attrs={"class": u"forecast-line__additionnal-mobile--rain-quantity"})[day].text
        # format 
        rain_mm = rain_mm.replace("\n", "").replace(" ", "").replace("pluie24h:", "")

        ##### Temperature #####
        # parse soup
        temper_morning = soup_15d.find_all("div", attrs={"class": u"forecast-line__pictos--temp"})[day * 2].text
        temper_evening = soup_15d.find_all("div", attrs={"class": u"forecast-line__pictos--temp"})[day * 2 + 1].text

        ##### Wind #####
        # parse soup
        wind = soup_15d.find_all("div", attrs={"class": u"forecast-line__additionnal-mobile--wind--direction"})[day].text
        # format 
        wind = wind.replace("\n", " ").replace("  ", "").replace("km/h ", "km/h")

        ##### Output #####
        # output
        output = ""
        output = output + "Pluie: " + rain + " (" + rain_mm + "). \n"
        output = output + "Température: " + temper_morning + \
            " - " + temper_evening + " °C. \n"
        output = output + "Vent: " + wind + ". \n"
        output = output + "Màj: " + last_update + ". "
        # format 
        output = output.replace("  ", " ")

        return output

def main(argv):
    """ Main function."""

    # handler object
    meteo = MeteoClass("meteo")

    # parse
    message = meteo.get_meteo(int(argv[1]))

    # print 
    print(message)


# Usage: python3 meteo.py <day_index> 
if __name__ == "__main__":
    main(sys.argv)
