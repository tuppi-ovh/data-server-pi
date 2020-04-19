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



import time
import sys
from datetime import datetime
from database import DataBaseClass
from mysensors import MySensorsClass


class CleanClass(DataBaseClass):
    """Clean database class."""

    def __init__(self, name, db_filename):
        DataBaseClass.__init__(self, name, db_filename)

    def clean_by_id(self, ident):
        """
        brief: Delete an element by ID. 
        param ident: must be an integer.
        """
        self._database_delete_entry_by_id(ident)
        self._database_commit()
        self.log_info("Database element deleted id=" + str(ident))

    def clean_debug(self):
        self._database_delete_entry_by_node_id(MySensorsClass.MYSENSORS_NODE_ID_DEBUG)
        self._database_commit()
        self.log_info("Debug elements deleted")

    def clean_vacuum(self):
        self._database_vacuum()
        self._database_commit()
        self.log_info("Compacted database")

    def clean_keep_peaks(self, period_str, place_str, var_str):
        # period
        if period_str == "month":
            timestamp_today = int(time.mktime(datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0).timetuple()))
            i_begin = 31
            i_end = 365
            step = 60 * 60 * 24
        elif period_str == "day":
            timestamp_today = int(time.mktime(datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0).timetuple()))
            i_begin = 1
            i_end = 30 * 24 + 1
            step = 60 * 60
        # place
        if place_str == "local":
            node_id = MySensorsClass.MYSENSORS_NODE_ID_LOCAL
        elif place_str == "ext":
            node_id = MySensorsClass.MYSENSORS_NODE_ID_EXT
        # variable
        if var_str == "temp":
            child_id = MySensorsClass.MYSENSORS_CHILD_ID_TEMP
            type_set = MySensorsClass.MYSENSORS_TYPE_SET_TEMP
        elif var_str == "hum":
            child_id = MySensorsClass.MYSENSORS_CHILD_ID_HUM
            type_set = MySensorsClass.MYSENSORS_TYPE_SET_HUM
        # loop
        counter = 0
        for i in range(i_begin, i_end):
            timestamp_begin = timestamp_today - i * step
            timestamp_end = timestamp_begin + step - 1
            if i == i_begin:
                timestamp_very_end = timestamp_end
            elif i == (i_end - 1):
                timestamp_very_begin = timestamp_begin
            entries = self._database_select_entries(
                node_id, child_id, type_set, timestamp_begin, timestamp_end)
            e_min = self._database_select_min_entry(
                node_id, child_id, type_set, timestamp_begin, timestamp_end)
            e_max = self._database_select_max_entry(
                node_id, child_id, type_set, timestamp_begin, timestamp_end)
            # delete elements by ID
            for e in entries:
                if e[0] != e_min[0][0] and e[0] != e_max[0][0]:
                    self._database_delete_entry_by_id(e[0])
                    counter = counter + 1
        self._database_commit()
        # log
        self.log_info("Keep peaks from " + str(timestamp_very_begin) + " to " + str(timestamp_very_end) +
              ", " + place_str + ", " + var_str + ": deleted " + str(counter) + " elements")

    def clean_auto(self):
        self.clean_debug()
        self.clean_keep_peaks("month", "local", "temp")
        self.clean_keep_peaks("month", "local", "temp")
        self.clean_keep_peaks("month", "local", "hum")
        self.clean_keep_peaks("month", "ext", "temp")
        self.clean_keep_peaks("month", "ext", "hum")
        self.clean_keep_peaks("day", "local", "temp")
        self.clean_keep_peaks("day", "local", "hum")
        self.clean_keep_peaks("day", "ext", "temp")
        self.clean_keep_peaks("day", "ext", "hum")


def main(argv):
    """Main function with arguments."""
    if len(argv) == 4 and argv[2] == "--id":
        clean = CleanClass("clean", argv[1])
        clean.clean_by_id(int(sys.argv[3]))
    elif len(argv) == 3 and argv[2] == "--debug":
        clean = CleanClass("clean", argv[1])
        clean.clean_debug()
    elif len(argv) == 3 and argv[2] == "--vacuum":
        clean = CleanClass("clean", argv[1])
        clean.clean_vacuum()
    elif len(argv) == 6 and argv[2] == "--peak":
        clean = CleanClass("clean", argv[1])
        clean.clean_keep_peaks(argv[3], argv[4], argv[5])
    elif len(argv) == 3 and argv[2] == "--auto":
        clean = CleanClass("clean", argv[1])
        clean.clean_auto()
    else:
        print("usage:")
        print("    python3 clean.py <database> <command> <parameter>")
        print("")
        print("commands with parameters:")
        print("    --help                      : print this message")
        print("    --id <id>                   : delete by ID")
        print("    --debug                     : delete all debug entries")
        print("    --peak <from> <place> <var> : clean entries from=day/month place=local/ext var=temp/hum")
        print("    --auto                      : delete entries automatically (debug, old, etc.)")
        print("    --vacuum                    : free space after deleting entries")
        print("")


# Execution: python3 clean.py <database> <command> <parameter>
if __name__ == "__main__":
    main(sys.argv)
