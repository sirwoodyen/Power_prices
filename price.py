import json
from datetime import date, datetime, timedelta, time
from urllib.request import urlopen
from pathlib import Path
from configparser import ConfigParser
from os import system
import os
import shutil
import time
import cursor
import logging

logging.basicConfig(filename="price.log", level=logging.DEBUG)
#logging.info("Program starting up - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

newday = False

#This is the config.ini file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)

#enable test stings
#teststrings - to show or hode those strings.
teststrings = config.getboolean("test", "teststrings")
testmode = config.getboolean("test", "testmode")
debugLogger = config.getboolean("test", "debuglogger")


#from config file, i feel it is self explainatory.
cursorhide = config.getboolean("app", "cursor_hide")

#if teststrings in config.ini file is true, then this function will be inviked.
def testdef(teststring):
    if teststrings == True:
        print(teststring)

#if debug/logging is activated in the config file. then this will be activated.
loggingstarted = False
def debug_logger(string):
    global  loggingstarted
    if debugLogger and loggingstarted == False:
        logging.info(string)
        loggingstarted = True
    elif debugLogger and loggingstarted == True:
        timestatement = " - Time: " + datetime.now().strftime("%H:%M:%S")
        output = timestatement + " - " + string
        logging.info(output)
    elif debugLogger and newday:
        #timestatement = " - New day started" + datetime.now().strftime("%Y-%m-%d")
        logging.info(string)

#function to clear the terminal window
#clear = lambda: system("cls") #this line is for windows, but then comment or delete the def clear() function.
def clear():
	os.system('clear')

if testmode:
    debug_logger(" - Program starting up - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Test mode"))
else:
    debug_logger(" - Program starting up - {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

#putting together some API stuff - do not change here! do it in the config.ini file!
if testmode:
    url = config["api-info"]["url_test"]
else:
    url = config["api-info"]["url"]
api_key = config["api-info"]["api_key"]
regions = ["zone=NO1", "zone=NO2", "zone=NO3", "zone=NO4", "zone=NO5", "zone=N06"]
selected_zone = regions[int(config["api-info"]["region"])]
today = str(datetime.now().date())
uri_api = str(url + selected_zone + "&date=" + today + "&key=" + api_key)
timestampjson = "%Y-%m-%dT%H:%M:%S"

#To recognize stamps
timestampStandard = "%Y-%m-%d %H:%M:%S"
timestamp_Clock = "%H:%M:%S"

#center my text.
def center_text(text):
    print(text.center(shutil.get_terminal_size().columns))
#json file stuff
if testmode:
    json_price_file = Path(config["file"]["json_file_testmode"])
else:
    json_price_file = Path(config["file"]["json_file"])
file_exist = False


#center all text
centertext = config.getboolean("app", "centertext")
textspace = config.getint("app", "textspace")

#get region
theregion = int(config["api-info"]["region"]) + 1

#loopcounter
counter = 0
jsonfile_updated = 0
jupdate = datetime.now().strftime(timestampStandard)

#checking if the json file exist, which it should be, after the first run.
def checkIfJasonExist():
    global file_exist
    if json_price_file.is_file():
        if teststrings == True:
            testdef("The json file exist")
        file_exist = True

# function to decode the timestamp from json file
def extract_ust(t):
    return datetime.strptime(t, timestampjson)
def extract_config_time(t):
    return datetime.strptime(t, timestampStandard)

# updating the config.ini file when changes are made
def updateconfig():
    with open(config_file, "w") as configfile:
        config.write(configfile)
        if teststrings == True:
            testdef("config value stored...\n")
            debug_logger("Config is updated")
#if it is a new day, it shall return True
def checkNeedUpdate():
    global today
    global jsonfile_updated
    global newday
    if testmode:
        dts = config["file"]["updated_testmode"]
    else:
        dts = config["file"]["updated"]
    checks = datetime.strptime(dts, "%Y-%m-%d %H:%M:%S").date()
    newdate = datetime.now()
    if checks.day != newdate.day:
        testdef(f"check day:{checks.day} newday:{newdate.day}")
        jsonfile_updated = jsonfile_updated + 1

        newday = True
        today = str(datetime.now().date())
        debug_logger("")
        debug_logger( "New day started - " + datetime.now().strftime("%Y-%m-%d"))

#this is THE program...
def runProgram():
    global newday
    global jupdate
    global today
    today = str(datetime.now().date())
    now = datetime.now()
    mytime = now.strftime(timestamp_Clock)
    testdef("Loop count: " + str(counter) + " - " + str(mytime))
    testdef("jfile update count: " + str(jsonfile_updated) + " - " + str(jupdate))
    checkIfJasonExist()
    if file_exist and newday == False:
        testdef("opening the " + str(json_price_file) + "\n")
        with open(json_price_file, "r") as fcc_file:
            data = json.load(fcc_file)
    else:
        with urlopen(uri_api) as response:
            debug_logger(f"fetching json from: {uri_api} - Zone: {theregion}")
            if file_exist == False:
                testdef("file did not exist... fetching data... make a new json file.")
                debug_logger("New json file is being created...")
            else:
                testdef("Updating json file...")
                debug_logger("Json file updated...")
            source = response.read()
            if testmode:
                config.set("file", "updated_testmode", str(datetime.now().strftime(timestampStandard)))
            else:
                config.set("file", "updated", str(datetime.now().strftime(timestampStandard)))
            updateconfig() # TODO check if the date actually gets updated in the ini file. seems like the testmode is, but not sure if the regular is.
            timecheck = datetime.now()
            jupdate = timecheck.strftime(timestampStandard)
            newday=False
        data = json.loads(source)
        with open(json_price_file, "w") as outfile:
            json.dump(data, outfile)
    
    for timestamp in data.keys():
        price = int((data[timestamp]["NOK_per_kWh"])*100)
        ts_from = extract_ust(data[timestamp]["valid_from"].split("+")[0])
        ts_to = extract_ust(data[timestamp]["valid_to"].split("+")[0])

        if ts_from.hour == datetime.now().hour and centertext == 0:
            print("price: " + str(price) + " øre" + " - Region:", int(config["api-info"]["region"])+1)
            print("Valid from: " + str(ts_from))
            print("Valid to: " + str(ts_to))
            print("\n")
            debug_logger(f"Price: {str(price)} øre")
        elif ts_from.hour == datetime.now().hour and centertext == 1:
            s0 = "\n\n\n\n"
            s1 = (f"Price: {str(price)} øre - Region: {theregion}")
            s2 = ("Valid from: " + str(ts_from))
            s3 = ("Valid to: " + str(ts_to))
            s4 = ("\n")
            center_text(s0)
            center_text(s1)
            center_text(s2)
            center_text(s3)
            print(s4.center(textspace))
            debug_logger(f"Price: {str(price)} øre")
            try:
                for timestamp in data.keys():
                    price_next = int((data[timestamp]["NOK_per_kWh"]) * 100)
                    ts_from = extract_ust(data[timestamp]["valid_from"].split("+")[0])
                    updatedtime = datetime.now().hour + 1

                    if ts_from.hour == updatedtime:
                        priceNextrHour = int((data[timestamp]["NOK_per_kWh"]) * 100)
                        print("\n")
                        center_text("Price next hour: " + str(priceNextrHour) + " øre" )
            except:
                text_except = "json is not updated to show next hour."
                debug_logger(" - Price for the next hour can not be shown.")
                center_text(text_except)

#Now, this will run the program in a loop
while True:
    if cursorhide:
        cursor.hide()
    else:
        cursor.show()
    clear()
    if testmode:
        print("Testmode Activated")
    #check if update of the json is needed
    checkNeedUpdate()
    runProgram()
    #this will make the loop count down and check again each hour. 
    dt = datetime.now() + timedelta(hours=1)
    dt = dt.replace(minute=1)
    while datetime.now() < dt:
        time.sleep(1)
    counter = counter + 1