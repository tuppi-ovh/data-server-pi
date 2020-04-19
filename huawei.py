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

# For more API calls just look on code in the huawei_lte_api/api folder, there is no separate DOC yet

import sys
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
from base import BaseClass
import config



class HuaweiClass(BaseClass):
    """
    brief: Main class.

    Available methods: 
    - Return month data usage  
    """

    def __init__(self, name):
        """
        Constructor.
        """
        BaseClass.__init__(self, name)

    def get_usage_gbytes(self):
        """
        """
        connection = AuthorizedConnection(config.HUAWEI_URL)
        stats = connection.get('monitoring/month_statistics')

        usage = (int(stats["CurrentMonthDownload"]) + int(stats["CurrentMonthUpload"])) / 1024 / 1024 / 1024

        return "{:.2f} GB".format(usage)        
        

def main(argv):
    """ Main function."""

    # handler object
    huawei = HuaweiClass("huawei")

    # print 
    print("usage: {:.2f} GB".format(huawei.get_usage_gbytes()))


# Usage: python3 huawei.py
if __name__ == "__main__":
    main(sys.argv)


