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
import sqlite3


class DataBaseClass(object):
    """Database management class."""

    # node id
    NODE_ID_LOCAL = 100
    NODE_ID_EXT = 103
    NODE_ID_VMC = 104
    NODE_ID_UNDERGROUND = 105
    NODE_ID_DEBUG = 133
    # child id
    CHILD_ID_TEMP = 0
    CHILD_ID_HUM = 1
    CHILD_ID_DEBUG = 33
    # cmd
    CMD_PRESENTATION = 0
    CMD_SET = 1
    # ack
    ACK_NONE = 0
    # type pres
    TYPE_PRES_TEMP = 6
    TYPE_PRES_HUM = 7
    TYPE_PRES_CUSTOM = 23
    TYPE_PRES_INFO = 36
    # type set
    TYPE_SET_TEMP = 0
    TYPE_SET_HUM = 1
    TYPE_SET_VAR1 = 24
    TYPE_SET_TEXT = 47
    TYPE_SET_CUSTOM = 48

    def __init__(self, db_filename):
        """ Constructor."""
        self.__db = sqlite3.connect(db_filename)
        self.__query_curs = self.__db.cursor()

    def _database_add_entry(
        self, timestamp, node_id, child_sensor_id, command, ack, typ, payload
    ):
        self.__query_curs.execute(
            """INSERT INTO MySensors (timestamp,node_id,
                                  child_sensor_id,command,ack,type,payload) VALUES (?,?,?,?,?,?,?)""",
            (timestamp, node_id, child_sensor_id, command, ack, typ, payload),
        )

    def _database_delete_entries_by_node_id(self, node_id):
        self.__query_curs.execute(
            """DELETE FROM MySensors WHERE node_id=?""", (node_id,)
        )

    def _database_last_entry(self, node_id, child_sensor_id, typ):
        self.__query_curs.execute(
            """SELECT timestamp, payload FROM MySensors WHERE node_id=? AND child_sensor_id=?
            AND type=? ORDER BY timestamp DESC LIMIT 1""",
            (node_id, child_sensor_id, typ),
        )
        return self.__query_curs.fetchall()

    def _database_commit(self):
        self.__db.commit()

    def _database_delete_entry_by_node_id(self, node_id):
        self.__query_curs.execute(
            """DELETE FROM MySensors WHERE node_id=?""", (node_id,)
        )

    def _database_delete_entry_by_id(self, entry_id):
        self.__query_curs.execute("""DELETE FROM MySensors WHERE id=?""", (entry_id,))

    def _database_vacuum(self):
        self.__query_curs.execute("""VACUUM""")

    def _database_select_entries(self, node_id, child_sensor_id, typ, ts_begin, ts_end):
        self.__query_curs.execute(
            """SELECT id, timestamp, payload FROM MySensors WHERE
                                  node_id=? AND child_sensor_id=? AND type=?
                                  AND timestamp>=? AND timestamp<=?""",
            (node_id, child_sensor_id, typ, ts_begin, ts_end),
        )
        return self.__query_curs.fetchall()

    def _database_select_min_entry(
        self, node_id, child_sensor_id, typ, ts_begin, ts_end
    ):
        self.__query_curs.execute(
            """SELECT id, timestamp, MIN(payload) FROM MySensors WHERE
                                  node_id=? AND child_sensor_id=? AND type=?
                                  AND timestamp>=? AND timestamp<=?""",
            (node_id, child_sensor_id, typ, ts_begin, ts_end),
        )
        return self.__query_curs.fetchall()

    def _database_select_max_entry(
        self, node_id, child_sensor_id, typ, ts_begin, ts_end
    ):
        self.__query_curs.execute(
            """SELECT id, timestamp, MAX(payload) FROM MySensors WHERE
                                  node_id=? AND child_sensor_id=? AND type=?
                                  AND timestamp>=? AND timestamp<=?""",
            (node_id, child_sensor_id, typ, ts_begin, ts_end),
        )
        return self.__query_curs.fetchall()

    def _database_create_table(self):
        """Create a table as node_id / child_sensor_id / command / ack / type / payload."""
        self.__query_curs.execute(
            """CREATE TABLE MySensors
                                  (id INTEGER PRIMARY KEY,timestamp INTEGER,node_id INTEGER,
                                  child_sensor_id INTEGER,command INTEGER,ack INTEGER,
                                  type INTEGER,payload REAL)"""
        )


def main(argv):
    """ Main function."""
    # handler object
    __ = DataBaseClass(argv[1])


# Usage: python3 telegram.py <database>
if __name__ == "__main__":
    main(sys.argv)
