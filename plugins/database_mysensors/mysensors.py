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

import time
import serial
from threading import Thread
from datetime import datetime
from .database import DataBaseClass


class ThreadSerialRecv(Thread):
    """Thread for serial data receive."""

    def __init__(self, port, commands, logs):
        Thread.__init__(self)
        self.__port = port
        if port != None:
            self.__serial = serial.Serial(port, baudrate=115200, timeout=1.0)
        self.__commands = commands
        self.__logs = logs
        self.__buffer = ""

    def run(self):

        # infinit loop
        while True:

            # concatenate to buffer
            if self.__port == None:
                self.__buffer += "1000;1;1;0;1;69.9\n1000;0;1;0;0;27.5\n"
                time.sleep(10)
            else:
                byt = self.__serial.read(256)
                string = byt.decode("ascii")
                self.__buffer += string

            # split elements
            buffer_separated = self.__buffer.split("\n")

            # append elements
            length = len(buffer_separated)
            for i in range(length - 1):
                self.__commands.append(buffer_separated[i])
                self.__logs.append(buffer_separated[i])

            # stock the last element if \n not found
            self.__buffer = buffer_separated[length - 1]

            # switch to another thread
            time.sleep(0)


class MySensorsClass(DataBaseClass):
    """MySensors class."""

    def __init__(self, port, db_filename):
        """ Constructor."""
        self.__port = port
        DataBaseClass.__init__(self, db_filename)

    def run(self):
        commands = []
        logs = []

        # thread for UART data receive
        thread_recv = ThreadSerialRecv(self.__port, commands, logs)
        # daemon mode for CTRL-C exits
        thread_recv.daemon = True
        # threads start
        thread_recv.start()

        # infinit loop
        while True:

            # stock logs
            length = len(logs)
            # loop on all logs
            for i in range(length):
                # extract an element
                element = logs[length - i - 1]
                del logs[length - i - 1]
                # log
                print(element)

            # number of commands
            length = len(commands)
            commit = False
            # loop on all commands
            for i in range(length):
                # timestamp
                timestamp = int(time.mktime(datetime.now().timetuple()))
                # extract an element
                element = commands[length - i - 1]
                del commands[length - i - 1]
                # parse
                element_separated = element.split(";")
                # write to database
                self._database_add_entry(
                    timestamp,
                    int(element_separated[0]),
                    int(element_separated[1]),
                    int(element_separated[2]),
                    int(element_separated[3]),
                    int(element_separated[4]),
                    float(element_separated[5]),
                )
                commit = True
            # commit database
            if commit:
                self._database_commit()
            # sleep
            time.sleep(1)
