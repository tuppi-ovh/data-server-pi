#!/bin/bash

# virtual env
source venv/bin/activate

# format
python3 -m black --exclude venv .

# check
python3 -m pylint --disable=R,C,W0603,W0702   \
                  data-server-pi \
                  data-server-pi.plugins.about \
                  data-server-pi.plugins.database_mysensors \
                  data-server-pi.plugins.huawei \
                  data-server-pi.plugins.meteo \
                  data-server-pi.plugins.vmc
