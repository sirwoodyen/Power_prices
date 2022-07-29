# Power_prices
checks and displays Norwgian powerprices

This is a program that is ment to check power prices in Norway.

I have used an RPi 2B+ for my project, with a 3,5" display for my project, font: Terminus size: 12*24.
To get youre own API key, send mail to "ffaildotwin@gmail.com".

I have set up a config.ini file, to fill this in.

if you want to do mutch testing, set the config.ini file in testmode, else you spam the real api, and api key might get deleted.
only get the the normal api json once a day. the tomorrows prices will be available each day at 14:00.

prizes and zones are so to speak accordingly to this page:
https://www.nordpoolgroup.com/en/Market-data1/Dayahead/Area-Prices/NO/Hourly/?dd=NO2&view=table
Zone-1=Oslo, Zone-2=Kristiansand, Zone-3=Bergen, Zone-4= Trondheim, Zone-5=Molde and Zone-6 = is Tromsø
Though in the config.ini file i have called this "region".


Ff you want to use this in windows, remove the clear() definition, and insert "clear = lambda: system("cls")" instead.
the rest should work  as long as you install the nessecary modules.
"cursor", " ConfigParser" and "pathlib" i think.




some nice to know stuff...


#this to make my LCD display work

sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git

chmod -R 755 LCD-show

cd LCD-show/

sudo ./LCD35-show


#configure font and size

sudo dpkg-reconfigure console-setup

