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

# https://dzone.com/articles/python-simple-http-server-with-cgi-scripts-enabled
# https://python.doctor/page-python-serveur-web-creer-rapidement


# Request format: http://127.0.0.1/cgi-bin/cgi_set.py?command=<command>&chat_id=<chat_id>

form = cgi.FieldStorage()
#print("Content-type: text/html; charset=utf-8\n")


mainc = main.MainClass()
mainc.execute(form.getvalue("command"), form.getvalue("chat_id"))


#print(form.getvalue("name"))
