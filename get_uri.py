from configparser import ConfigParser

# This is the config.ini file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

testmode = config.getboolean("test", "testmode")


def Get_URI(today):
    # putting together some API stuff - do not change here! do it in the config.ini file!
    if testmode:
        url = config["api-info"]["url_test"]
    else:
        url = config["api-info"]["url"]
    api_key = config["api-info"]["api_key"]
    regions = ["zone=NO1", "zone=NO2", "zone=NO3", "zone=NO4", "zone=NO5", "zone=N06"]
    selected_zone = regions[int(config["api-info"]["region"])]
    uri_api = str(url + selected_zone + "&date=" + today + "&key=" + api_key)
    return uri_api
