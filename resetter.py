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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

#Config
#---------------------
DEFAULT_FILE_NAME_DATA = "login_data.json"
DELAY_ELEMENT = 10

#Helpers
#---------------------

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

    

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
parser.add_argument("-c","--cred", nargs='?', default=DEFAULT_FILE_NAME_DATA ,help='Specify credentials. Overrides json file.')
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
	raise ValueError("Archivo de datos no encontrado.")
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
		raise ValueError("El driver elegido no es un driver valido.")
		sys.exit()
else:	#windows
	print("Running on Windows. Using default webdriver.")
	print("Using webdriver: %s" %args.driverdir)
	mydriver = webdriver.Firefox()


#Do the work
#---------------------------------------------------------------
mydriver.get(baseurl)
mydriver.maximize_window()
url_login = mydriver.current_url;
print("Entering %s" %url_login)
print("")
#Clear Username TextBox if already allowed "Remember Me" & Write Username
try:
    usernameTxtBox = WebDriverWait(mydriver, DELAY_ELEMENT).until(
            lambda driver : driver.find_element_by_xpath(xpaths['usernameTxtBox'])
    )
    print("Username textbox located")
except TimeoutException:
    print ("Loading took too much time!")
    raise ValueError("Username textbox does not exist.")
usernameTxtBox.clear()
usernameTxtBox.send_keys(username)
print("Username cleared and written.")
print("-")

#Clear Password TextBox if already allowed "Remember Me" & Write Password
try:
    passwordTxtBox = WebDriverWait(mydriver, DELAY_ELEMENT).until(
            lambda driver : driver.find_element_by_xpath(xpaths['passwordTxtBox'])
    )
    print("Password textbox located")
except TimeoutException:
    print ("Loading took too much time!")
    raise ValueError("Password textbox does not exist.")
passwordTxtBox.clear()
passwordTxtBox.send_keys(password)
print("Password cleared and written.")
print("-")

#Locate and click Login button
try:
    submitButton = WebDriverWait(mydriver, DELAY_ELEMENT).until(
            lambda driver : driver.find_element_by_xpath(xpaths['submitButton'])
    )
    print("Submit button located")
except TimeoutException:
    print ("Loading took too much time!")
    raise ValueError("Submit button does not exist.")
submitButton.click()
print("Submited.")
print("")

#Redirecting to homepage
url_homepage = mydriver.current_url;
if ( url_homepage != url_login):
	print("Redirected to %s" %url_homepage)
#Check existence and click Reset button
try:
    resetButton = WebDriverWait(mydriver, DELAY_ELEMENT).until(
            lambda driver : driver.find_element_by_xpath(xpaths['resetButton'])
    )
    print("Reset button located")
except TimeoutException:
    print ("Loading took too much time!")
    raise ValueError("Reset button does not exist. Possible wrong credentials.")
resetButton.click()
print("Clicked reset button.")
print("")

print("Success!")
print("")