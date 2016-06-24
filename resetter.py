#ScriptName : resetter.py
#---------------------
import sys 							#to accept argv
import argparse						#to parse argv
import platform						#to detect linux or windows
import json							#to parse username and password
import os.path
from pprint import pprint			#for pretty print
from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

#Config
#---------------------
DEFAULT_FILE_NAME_DATA = "login_data.json"


#Code
#---------------------
print("")
print("Starting DIR300 Resetter...")
print("")

#parse argv
parser = argparse.ArgumentParser(description='Dir300 resetter script.')
parser.add_argument("-d","--driver", nargs='?', default="firefox",help='Choose a webdriver.')
parser.add_argument("-D","--driverdir", nargs='?', default="",help='Specify webdriver directory.')
parser.add_argument("-f","--file", nargs='?', default=DEFAULT_FILE_NAME_DATA ,help='Specify json data file.')
args=parser.parse_args()
print("Going to use webdriver: "+ args.driver)
if args.driverdir != "":
    print ("Driverdir has been set (value is %s)" % args.driverdir)
#detect data file (json)
if os.path.isfile(args.file):
	with open(args.file) as data_file:    
	    data = json.load(data_file)
	    print("")
	    print("Loaded file %s" %args.file)
	    print("Username: "+data["username"])
	    print("Password: "+data["password"])
	    print("")

else:
	print("Buscando el archivo "+args.file)
	print("Archivo de datos no encontrado.")
	sys.exit()


#Set variables
baseurl = "http://localhost/index.php"
username = data["username"]
password = data["password"]
xpaths = { 'usernameTxtBox' : "//input[@name='username']",
           'passwordTxtBox' : "//input[@name='password']",
           'submitButton' :   "//input[@name='login']",
           'resetButton'  :	  "//button[@name='button']"
         }

#Detect OS to choose webdriver
if ( platform.system() == "Linux" ):
	if (args.driver == "phantomjs"):
		if args.driverdir is not "":
			mydriver = webdriver.PhantomJS(args.driverdir)
		else:
			mydriver = webdriver.PhantomJS()
	elif (args.driver == "firefox"):
		if args.driverdir is not "":
			mydriver = webdriver.Firefox(args.driverdir)
		else:
			mydriver = webdriver.Firefox()
	else:
		print("Wrong webdriver.")
		sys.exit()
else:	#windows
	print("Running on Windows. Using default webdriver.")
	print("Using webdriver: %s" %args.driverdir)
	mydriver = webdriver.Firefox()


#Do the work
mydriver.get(baseurl)
mydriver.maximize_window()
#Clear Username TextBox if already allowed "Remember Me" & Write Username
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)
print("Username cleared and written.")

#Clear Password TextBox if already allowed "Remember Me" & Write Password
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)
print("Password cleared and written.")

#Click Login button
mydriver.find_element_by_xpath(xpaths['submitButton']).click()
print("Submited.")

#Redirecting to homepage
print("Redirected.")
#Click Reset button
mydriver.find_element_by_xpath(xpaths['resetButton']).click()
print("Clicked reset button.")
print("")

print("Success!")
print("")