#!/usr/bin/python3

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

import cgi
import main


# Request format: http://127.0.0.1/cgi-bin/cgi_set.py?command=<command>&chat_id=<chat_id>
form = cgi.FieldStorage()
command = form.getvalue("command")
chat_id = int(form.getvalue("chat_id"))

# execute
mainc = main.MainClass()
result = mainc.execute_from_cgi(command, chat_id)

# print on html page 
print("\nExecution result:\n")
print(result)

