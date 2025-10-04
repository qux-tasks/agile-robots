import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.ini")

config = ConfigParser()
read_files = config.read(CONFIG_PATH)

# connection
url = config["connection"]["url"]

# user data
username = config["user_data"]["username"]
password = config["user_data"]["password"]

# endpoints
auth_endpoint = f"{url}/auth"
booking_endpoint = f"{url}/booking"