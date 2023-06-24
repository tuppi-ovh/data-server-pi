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

# imports
import time
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
from .database import DataBaseClass


# graph colors
colorlist = {}
colorlist[DataBaseClass.NODE_ID_LOCAL] = "red"
colorlist[DataBaseClass.NODE_ID_EXT] = "blue"
colorlist[DataBaseClass.NODE_ID_VMC] = "green"
colorlist[DataBaseClass.NODE_ID_BASEMENT] = "black"

# node name list
nodenamelist = {}
nodenamelist[DataBaseClass.NODE_ID_LOCAL] = "local"
nodenamelist[DataBaseClass.NODE_ID_EXT] = "ext"
nodenamelist[DataBaseClass.NODE_ID_VMC] = "vmc"
nodenamelist[DataBaseClass.NODE_ID_BASEMENT] = "basement"

# child name list
childnamelist = {}
childnamelist[DataBaseClass.CHILD_ID_TEMP] = "temper"
childnamelist[DataBaseClass.CHILD_ID_HUM] = "hum"


class ExecClass:
    """ Class to stock execution arguments."""

    def __init__(self, node_id, child_sensor_id, typ, duration, filename):
        self.node_id = node_id
        self.child_sensor_id = child_sensor_id
        self.type = typ
        self.duration = duration
        self.filename = filename


class StatisticsClass(DataBaseClass):
    def __init__(self, db_filename):
        """ Constructor."""
        DataBaseClass.__init__(self, db_filename)

    def __timestamp_begin_calc(self, ts_now, duration_str):
        """ Returns timestamp begin for the selected type of output (1d, 1m, 1y)."""
        # numeric value
        value = int(re.search(r"\d+", duration_str).group())
        # convert string to a factor
        if duration_str.find("y") > 0:
            value *= 365 * 24 * 60 * 60
        elif duration_str.find("m") > 0:
            value *= 30 * 24 * 60 * 60
        elif duration_str.find("w") > 0:
            value *= 7 * 24 * 60 * 60
        elif duration_str.find("d") > 0:
            value *= 24 * 60 * 60
        elif duration_str.find("h") > 0:
            value *= 60 * 60
        else:
            value *= 1
        # return
        return ts_now - value

    def update_temperature(self, duration_str):
        """ Updates last value temperature. """
        nodelist = [
            self.NODE_ID_LOCAL,
            self.NODE_ID_EXT,
            self.NODE_ID_VMC,
            self.NODE_ID_BASEMENT,
        ]
        exec_struct = ExecClass(
            nodelist,
            self.CHILD_ID_TEMP,
            self.TYPE_SET_TEMP,
            duration_str,
            "img_temper_" + duration_str + ".png",
        )
        return self.update(exec_struct)

    def update_humidity(self, duration_str):
        """ Updates last value humidity. """
        nodelist = [
            self.NODE_ID_LOCAL,
            self.NODE_ID_EXT,
            self.NODE_ID_VMC,
            self.NODE_ID_BASEMENT,
        ]
        exec_struct = ExecClass(
            nodelist,
            self.CHILD_ID_HUM,
            self.TYPE_SET_HUM,
            duration_str,
            "img_hum_" + duration_str + ".png",
        )
        return self.update(exec_struct)

    def update(self, exec_value):
        """ Returns a graph with one type of data from several  sources.
        Example: temperature internal & external.
        """
        # return value
        retval = None
        # current time
        ts_now = int(time.mktime(datetime.now().timetuple()))
        # exec
        e = exec_value
        # two treatments regarding duration
        if e.duration != "0":
            # loop on all nodes
            for n in e.node_id:
                dates = []
                values = []
                # extract values
                data = self._database_select_entries(
                    n,
                    e.child_sensor_id,
                    e.type,
                    self.__timestamp_begin_calc(ts_now, e.duration),
                    ts_now,
                )
                for d in data:
                    dates.append(datetime.fromtimestamp(d[1]))
                    values.append(d[2])
                plt.plot(dates, values, label=nodenamelist[n], color=colorlist[n])
            # plot
            plt.legend(loc="upper left")
            plt.gcf().autofmt_xdate()
            plt.savefig(e.filename)
            # clear for the next iteration
            plt.clf()
            # return value
            retval = e.filename

        else:
            data = {}
            data["1-sensor-place"] = []
            data["2-" + childnamelist[e.child_sensor_id]] = []
            data["3-last-update"] = []
            # loop on all nodes
            for n in e.node_id:
                try:
                    db_data = self._database_last_entry(n, e.child_sensor_id, e.type)
                    value_str = "%.1f" % db_data[0][1]
                    data["1-sensor-place"].append(nodenamelist[n])
                    data["3-last-update"].append(datetime.fromtimestamp(db_data[0][0]))
                    data["2-" + childnamelist[e.child_sensor_id]].append(value_str)
                except:
                    print("[statistics] last entry not found")

            # Convert the dictionary into DataFrame (in alphabetic order!)
            df = pd.DataFrame(data)

            # format: no frame, no axes
            ax = plt.subplot(111, frame_on=False)  # no visible frame
            ax.xaxis.set_visible(False)  # hide the x axis
            ax.yaxis.set_visible(False)  # hide the y axis

            # plot table
            tbl = plt.table(
                cellText=df.values,
                rowLabels=df.index,
                colLabels=df.columns,
                cellLoc="center",
                rowLoc="center",
                loc="center",
            )
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(24)
            tbl.scale(4, 4)
            plt.savefig(e.filename, bbox_inches="tight", pad_inches=0.05)
            # clear for the next iteration
            plt.clf()
            # return value
            retval = e.filename

        return retval


def main(argv):
    """Main function with arguments."""
    # check args
    if len(argv) >= 2:
        # handler object
        statistics = StatisticsClass(argv[1])
        # execute all
        statistics.update_temperature("0")
        statistics.update_temperature("1d")
        statistics.update_temperature("1w")
        statistics.update_temperature("1m")
        statistics.update_temperature("1y")
        statistics.update_humidity("0")
        statistics.update_humidity("1d")
        statistics.update_humidity("1w")
        statistics.update_humidity("1m")
        statistics.update_humidity("1y")
    else:
        print("Error")


# declaration for pandas timestamp
register_matplotlib_converters()

# Standalone execution: python3 statistics.py <database>
# Example: python3 .\github\data-server-pi\statistics.py .\MySensors.db
if __name__ == "__main__":
    main(sys.argv)
