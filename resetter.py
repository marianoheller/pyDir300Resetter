#ScriptName : resetter.py
#TODO: 
#		wifi connect
#		make deamon that resets only when not pinging
#---------------------
import sys 							#to accept argv
import argparse						#to parse argv
import platform						#to detect linux or windows
import json							#to parse username and password
import os.path						#to check if file exists
import textwrap
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
DELAY_ELEMENT = 50

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
availableWebDrivers =	"Available webdrivers: \n" \
					 	"\tFirefox, \n\tFirefoxProfile, \n\tChrome, " \
 						"\n\tChromeOptions, \n\tIe, \n\tOpera, " \
 						"\n\tPhantomJS, \n\tRemote, \n\tDesiredCapabilities, " \
 						"\n\tActionChains, \n\tTouchActions, \n\tProxy"

#parse argv
parser = argparse.ArgumentParser(description='Dir300 resetter script.',epilog=availableWebDrivers)
parser.add_argument("-d","--driver", nargs='?', default="firefox",help='Choose a webdriver.')
parser.add_argument("-D","--driverdir", nargs='?', default="",help='Specify webdriver directory. REQUIRED with phantomJS on windows.')
parser.add_argument("-f","--file", nargs='?', default=DEFAULT_FILE_NAME_DATA ,help='Specify json data file.')
parser.add_argument("-c","--cred", nargs='?',help='Specify credentials. Overrides json file. Format user:password')
args=parser.parse_args()
print("Going to use webdriver: "+ args.driver)
if args.driverdir != "":
    print ("Driverdir has been set (value is %s)" % args.driverdir)

if args.cred is not None:
	if (len(args.cred.split(":")) >= 2):
		lista = args.cred.split(":")
		data = {}
		data["username"] = lista[0]
		data["password"] = lista[1]
	else:
		print("Formate de credencial incorrecto. [user:password]")
		print("Se ingreso: %s" %args.cred)
		raise ValueError("Archivo de datos no encontrado.")
		sys.exit()
else:	
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
baseurl = "http://192.168.0.1/login.php"
username = data["username"]
password = data["password"]
# xpaths = { 'usernameTxtBox' : "//input[@name='username']",
#            'passwordTxtBox' : "//input[@name='password']",
#            'submitButton' :   "//input[@name='login']",
#            'resetButton'  :	  "//button[@name='button']"
#          }
xpaths = { 'usernameTxtBox' : 	"id('box_header')/x:center/x:table/x:tbody/x:tr[1]/x:td[2]/x:input",
            'passwordTxtBox' : 	"id('box_header')/x:center/x:table/x:tbody/x:tr[2]/x:td[2]/x:input",
            'submitButton' :  	"id('box_header')/x:center/x:table/x:tbody/x:tr[2]/x:td[3]/x:input",
            'resetButton'  :	"id('sidenav_container')/x:table/x:tbody/x:tr[2]/x:td/x:table/x:tbody/x:tr/x:td/x:input"
          }

xpaths = { 	'usernameTxtBox' : 	"//td[@id='box_header']/center/table/tbody/tr[1]/td[2]/input",
			'passwordTxtBox' : 	"//td[@id='box_header']/center/table/tbody/tr[2]/td[2]/input",
			'submitButton' :  	"//td[@id='box_header']/center/table/tbody/tr[2]/td[3]/input",
			'resetButton'  :	"//td[@id='sidenav_container']/table/tbody/tr[2]/td/table/tbody/tr/td/input",
			'countdownMarker' : "//td[@id='box_header']/center/table/tbody/tr[1]/td/input"
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
	if (args.driver == "phantomjs"):
		if args.driverdir is not "":
			mydriver = webdriver.PhantomJS(args.driverdir)
		else:
			print("PhantomJS on windows requiers path.")
			raise ValueError("PhantomJS on windows requiers -D option.")
			sys.exit()
	elif (args.driver == "firefox"):
		if args.driverdir is not "":
			mydriver = webdriver.Firefox(args.driverdir)
		else:
			mydriver = webdriver.Firefox()
	elif (args.driver == "chrome"):
		if args.driverdir is not "":
			mydriver = webdriver.Chrome(args.driverdir)
		else:
			mydriver = webdriver.Chrome()
	else:
		print("Wrong webdriver.")
		raise ValueError("El driver elegido no es un driver valido.")
		sys.exit()


#Do the web scraping
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


try:
    WebDriverWait(mydriver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = mydriver.switch_to_alert()
    alert.accept()
    print ("alert accepted")
except TimeoutException:
    print ("no alert")


#Locate and click Login button
try:
    countdownMarker = WebDriverWait(mydriver, DELAY_ELEMENT).until(
            lambda driver : driver.find_element_by_xpath(xpaths['countdownMarker'])
    )
    print("Submit button located")
    print("")
    print("Success!")
    mydriver.quit()
except TimeoutException:
    print ("Loading took too much time!")
    raise ValueError("Submit button does not exist.")


