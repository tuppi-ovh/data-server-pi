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
from datetime import datetime
from .database import DataBaseClass


class AddClass(DataBaseClass):
    """Clean database class."""

    def __init__(self, db_filename):
        DataBaseClass.__init__(self, db_filename)

    def add_temper(self, node_id, temper):
        # timestamp
        timestamp = int(time.mktime(datetime.now().timetuple()))
        # write to database
        self._database_add_entry(timestamp, node_id, self.CHILD_ID_TEMP, self.CMD_SET,
                                    self.ACK_NONE, self.TYPE_SET_TEMP, temper)
        self._database_commit()                                    

    def add_humidity(self, node_id, humidity):
        # timestamp
        timestamp = int(time.mktime(datetime.now().timetuple()))
        # write to database
        self._database_add_entry(timestamp, node_id, self.CHILD_ID_HUM, self.CMD_SET,
                                    self.ACK_NONE, self.TYPE_SET_HUM, humidity)
        self._database_commit()