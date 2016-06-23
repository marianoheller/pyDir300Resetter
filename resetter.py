#ScriptName : Login.py
#---------------------
import sys
from selenium import webdriver


#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


baseurl = "http://localhost/index.php"
username = "admin"
password = "admin"
xpaths = { 'usernameTxtBox' : "//input[@name='username']",
           'passwordTxtBox' : "//input[@name='password']",
           'submitButton' :   "//input[@name='login']",
           'resetButton'  :	  "//button[@name='button']"
         }

mydriver = webdriver.Firefox()
mydriver.get(baseurl)
mydriver.maximize_window()

#Clear Username TextBox if already allowed "Remember Me" 
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()

#Write Username in Username TextBox
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)

#Clear Password TextBox if already allowed "Remember Me" 
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()

#Write Password in password TextBox
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)

#Click Login button
mydriver.find_element_by_xpath(xpaths['submitButton']).click()

#Redirecting to homepage
#Click Reset button
mydriver.find_element_by_xpath(xpaths['resetButton']).click()