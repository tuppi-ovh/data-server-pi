# Introduction

Data Server STM32 is a high level application for the Smart Home data acquisition.

# Related Projects

For hardware description refer to https://tuppi.ovh/data_server_stm32/doc_data_server.

For low level application refer to https://github.com/tuppi-ovh/data-server-stm32. 

# Python Project

### Dependecies

Python > 3.5 is requered.

It is required to install these packages:
- pandas by `python3 -m pip install pandas`
- BeautifulSoup by `python3 -m pip install bs4`
- matplotlib by `python3 -m pip install matplotlib`
- huawei_lte_api by `python3 -m pip install huawei_lte_api`
- serial interface:
    - if Linux by `sudo apt-get update; sudo apt-get install python-serial python3-serial`
    - if Windows by `python3 -m pip install serial`

If you have a problem with `numpy` : 
```sh
python3 -m pip uninstall numpy
python3 -m pip install numpy
sudo apt-get install libatlas-base-dev
```

### Configuration File

It is necessary to add some configuration data to `config.py` file:

```py
# Log enabled flag
BASE_LOG_FILE_ENABLED = False

# Local file for logs (here in RAM FS)
BASE_LOG_FILENAME = "/run/log/data-server-pi.log"

# Telegram Bot token 
TELEGRAM_BOT_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# List of authorized telegram chat IDs
TELEGRAM_CHAT_ID_LIST = (xxxx, yyyy, zzzz)

# URL to Huawei modem. Login is "admin". Password is "admin". 
HUAWEI_URL = "http://admin:admin@192.168.0.1/"

# URL to prefered meteo site 
METEO_URL = "http://xxxxxxxxxxxxxxxx.com"
```

# License

Refer to the [LICENSE](LICENSE) file.
