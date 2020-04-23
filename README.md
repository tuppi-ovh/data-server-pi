# Introduction

Data Server STM32 is a high level application for the Smart Home data acquisition. 
This project should be run on Raspberry PI board.

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

### Project Structure

Inheritance:
```plantuml
@startuml
DataBaseClass <|-- CleanClass
BaseClass <|-- DataBaseClass
BaseClass <|-- HuaweiClass
BaseClass <|-- MainClass
BaseClass <|-- MeteoClass
DataBaseClass <|-- MySensorsClass
BaseClass <|-- StatisticsClass
BaseClass <|-- TelegramClass
@enduml
```

Dependencies: 
```plantuml
@startuml
rectangle "main.py" as MAIN 
rectangle "meteo.py" as METEO
rectangle "config.py" as CONFIG
rectangle "telegram.py" as TELEGRAM
rectangle "statistics.py" as STATISTICS
rectangle "huawei.py" as HUAWEI
rectangle "clean.py" as CLEAN
rectangle "mysensors.py" as MYSENSORS
rectangle "base.py" as BASE
rectangle "database.py" as DATABASE

MAIN --> METEO
MAIN --> TELEGRAM
MAIN --> HUAWEI
MAIN --> STATISTICS
MAIN --> CLEAN
MAIN --> MYSENSORS

METEO --> CONFIG
TELEGRAM --> CONFIG
BASE --> CONFIG
HUAWEI --> CONFIG

CLEAN --> DATABASE 
DATABASE --> BASE
HUAWEI --> BASE
MAIN --> BASE
METEO --> BASE
MYSENSORS --> DATABASE
STATISTICS --> BASE 
TELEGRAM --> BASE 

@enduml
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

# Systemd Services

It is necessary to launch some systemd services to have a Telegram connection 
with your Raspberry PI all the time:
- Telegram Service: to be able to receive telegram messages.
- MySensors Service: to be able to receive STM32 data (temperature, humidity).
- HTTP server: to be able to pass commands to devices based on ESP8266.

### Telegram Service 

Create a file `/lib/systemd/system/data-server-pi-telegram.service` with this content:

```ini
[Unit]
Description=MySensors Telegram Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /absulut/path/to/the/project/main.py /absulut/path/to/the/project/MySensors.db auto -1
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

Launch the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable data-server-pi-telegram.service
sudo systemctl start data-server-pi-telegram.service
sudo systemctl status data-server-pi-telegram.service
```

### MySensors Service (Connection with STM32)

Create a file `/lib/systemd/system/data-server-pi-mysensors.service` with this content:

```ini
[Unit]
Description=MySensors Main Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /absulut/path/to/the/project/main.py /absulut/path/to/the/project/MySensors.db mysensors-dont-call-from-telegram -1
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

Launch the service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable data-server-pi-mysensors.service
sudo systemctl start data-server-pi-mysensors.service
sudo systemctl status data-server-pi-mysensors.service
```


### HTTP Server

Create a file `/lib/systemd/system/data-server-linux-httpd.service` with this content:

```ini
[Unit]
Description=MySensors HTTP Server
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
WorkingDirectory=/path/to/http/files/www
ExecStart=/usr/bin/python3 -m http.server 80
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

Launch the service:
```sh
sudo systemctl daemon-reload
sudo systemctl enable data-server-pi-httpd.service
sudo systemctl start data-server-pi-httpd.service
sudo systemctl status data-server-pi-httpd.service
```

# License

Refer to the [LICENSE](LICENSE) file.
