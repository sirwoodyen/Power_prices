import json
from datetime import datetime
from debugger import debug_logger
from configparser import ConfigParser
from pathlib import Path
from clear import clear_screen
import shutil
import cursor

# config file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

test_mode = config.getboolean("test", "testmode")
selected_region = int(config["api-info"]["region"]) + 1
cursor_hide = config.getboolean("app", "cursor_hide")

timestamp_json = "%Y-%m-%dT%H:%M:%S"

# bool value if json file exist
file_exist = False
if test_mode:
    json_price_file = Path(config["file"]["json_file_testmode"])
else:
    json_price_file = Path(config["file"]["json_file"])


def extract_ust(t):
    return datetime.strptime(t, timestamp_json)


# Center my text.
def center_text(text):
    print(text.center(shutil.get_terminal_size().columns))


def center_text_block(text):
    for line in text.splitlines():
        print(line.center(shutil.get_terminal_size().columns))


def run():
    if cursor_hide:
        cursor.hide()
    clear_screen()
    with open(json_price_file, "r") as fcc_file:
        data = json.load(fcc_file)

        for timestamp in data.keys():
            price = int((data[timestamp]["NOK_per_kWh"]) * 100)
            ts_from = extract_ust(data[timestamp]["valid_from"].split("+")[0])
            ts_to = extract_ust(data[timestamp]["valid_to"].split("+")[0])

            if ts_from.hour == datetime.now().hour:
                display_text = "\n\n\n\n" \
                               f"price: {str(price)} øre - Region: {selected_region}\r" \
                               f"Valid from: {str(ts_from)}\r" \
                               f"Valid to: {str(ts_to)}\r" \
                               f"\n\n"

                try:
                    for timestamp in data.keys():
                        ts_from = extract_ust(data[timestamp]["valid_from"].split("+")[0])
                        updatedtime = datetime.now().hour + 1

                        if ts_from.hour == updatedtime:
                            priceNextrHour = int((data[timestamp]["NOK_per_kWh"]) * 100)
                            display_text_add = f"\nPrice next hour: {str(priceNextrHour)} øre\r"
                            display_text = display_text + display_text_add
                except:
                    display_text = display_text + "json is not updated to show next hour.\r"
                    debug_logger("Price for the next hour can not be shown.")

                center_text_block(display_text)
                debug_logger(f"Price is: {str(price)} øre")