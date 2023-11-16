import os
NAME = "txttable"
VERSION = "0.1.0"
HOME_DIR = os.path.expanduser("~")
USER_DATA_DIR = os.path.join(HOME_DIR, f".{NAME}/")
USER_CONFIG_PATH = os.path.join(USER_DATA_DIR, 'config.json')
