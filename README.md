# Introduction

Data Server STM32 is a high level application for the Smart Home data acquisition. 
This project should be run on Raspberry PI board.


# Python Project

### Dependecies

Python > 3.5 is requered.

It is required to install packages:
- main dependecies: `python3 -m pip install -r requirements.txt`
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
# Absolut path to MySensors database
MYSENSORS_DATABASE_FILENAME = "/absolut/path/to/database/MySensors.db"

# MySensors COM port
MYSENSORS_SERIAL_PORT = "/dev/ttyUSB0"

# Telegram Bot token 
TELEGRAM_BOT_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# List of authorized telegram chat IDs
TELEGRAM_CHAT_ID_LIST = (xxxx, yyyy, zzzz)

# URL to Huawei modem. Login is "admin". Password is "admin". 
HUAWEI_URL = "http://admin:admin@192.168.0.1/"

# URL to prefered meteo site 
METEO_URL = "http://xxxxxxxxxxxxxxxx.com"

# Absolut path to vmc web server
VMC_WWW_PATH = "/absolut/path/to/webserver/www"

# Enabled plugins (about is forced to be enabled)
MAIN_PLUGINS = ["meteo", "mysensors", "huawei", "mysensors"]
```


# HTTP Server

To be able to tun correclty the http server you should:
- create a `www` folder inside the project folder
- create a `www/cgi-bin` folder
- create a symlink `ln -s /absolut/path/to/project/cgi_cmd.py www/cgi-bin/cgi_cmd.py`  
- make `cgi_cmd.py` executable by `chmod a+x cgi_cmd.py`
- add all necessary rights by `chmod 777 <filename>` to files like `MySensors.db` to have an access from cgi


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
Description=Data Server Telegram Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /absulut/path/to/the/project/__init__.py auto -1
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
Description=Data Server MySensors Daemon
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /absulut/path/to/the/project/__init__.py mysensors-dont-call-from-telegram -1
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

Create a file `/lib/systemd/system/data-server-pi-httpd.service` with this content:

```ini
[Unit]
Description=Data Server HTTP Daemon
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
WorkingDirectory=/path/to/http/files/www
ExecStart=/usr/bin/python3 -m http.server --cgi 80
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

# Message Automatization with CRON

We add this line by `sudo crontab -e`:
```
0 21 * * * /usr/bin/python3 /absulut/path/to/the/project/__init__.py <command> <chat_id>
```

# References

- Hardware description: https://tuppi.ovh/data_server_stm32/doc_data_server.
- Low level application (STM32): https://github.com/tuppi-ovh/data-server-stm32. 
- Web page of this project: https://tuppi.ovh/data_server_pi/doc_data_server_pi.


# License

Refer to the [LICENSE](LICENSE) file.
