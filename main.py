from datetime import date, datetime, timedelta, time
from get_uri import Get_URI
from get_json import download
from pathlib import Path
from configparser import ConfigParser
from debugger import debug_logger
from display import run
import time

# config file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

# config loading
cursorhide = config.getboolean("app", "cursor_hide")
testmode = config.getboolean("test", "testmode")
debugLogger = config.getboolean("test", "debuglogger")

# timestamp standards
timestampStandard = "%Y-%m-%d %H:%M:%S"
timestamp_Clock = "%H:%M:%S"

# bool value if json file exist
file_exist = False
if testmode:
    json_price_file = Path(config["file"]["json_file_testmode"])
else:
    json_price_file = Path(config["file"]["json_file"])


def extract_config_time(t):
    return datetime.strptime(t, timestampStandard)


def check_if_json_exist():
    global file_exist
    if json_price_file.is_file():
        debug_logger("The json file exist")
        file_exist = True
    else:
        download(Get_URI(str(datetime.now().date())))
        debug_logger("New json is downloaded.")


def check_startup_date():
    if testmode:
        dts = config["file"]["updated_testmode"]
    else:
        dts = config["file"]["updated"]
    checks = datetime.strptime(dts, "%Y-%m-%d %H:%M:%S").date()
    newdate = datetime.now()
    if checks.day != newdate.day:
        debug_logger( "New day started since last time - " + datetime.now().strftime("%Y-%m-%d"))
        download(Get_URI(str(datetime.now().date())))


def my_timer():
    dt = datetime.now() + timedelta(hours=1)
    dt = dt.replace(minute=2)
    while datetime.now() < dt:
        time.sleep(1)


def main():
    check_startup_date()
    time_before = datetime.now().date()
    check_if_json_exist()
    while True:
        time_after = datetime.now().date()
        if time_before != time_after:
            download(Get_URI(str(datetime.now().date())))
            time_before = datetime.now().date()
            debug_logger("New day started - " + datetime.now().strftime("%Y-%m-%d"))
        run()
        my_timer()


if __name__ == "__main__":
    main()
