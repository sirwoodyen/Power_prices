from urllib.request import urlopen
from configparser import ConfigParser
import json
from datetime import datetime
from pathlib import Path

# This is the config.ini file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

testmode = config.getboolean("test", "testmode")

timestampStandard = "%Y-%m-%d %H:%M:%S"

if testmode:
    json_price_file = Path(config["file"]["json_file_testmode"])
else:
    json_price_file = Path(config["file"]["json_file"])


def update_config():
    from debugger import debug_logger
    with open(config_file, "w") as configfile:
        config.write(configfile)
        debug_logger("Config is updated")


def download(uri_api):
    with urlopen(uri_api) as response:
        source = response.read()
        data = json.loads(source)
        with open(json_price_file, "w") as outfile:
            json.dump(data, outfile)

    if testmode:
        config.set("file", "updated_testmode", str(datetime.now().strftime(timestampStandard)))
    else:
        config.set("file", "updated", str(datetime.now().strftime(timestampStandard)))
    update_config()
