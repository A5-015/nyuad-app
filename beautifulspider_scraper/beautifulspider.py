import time #generally useful
import os  #generally useful

from bs4 import BeautifulSoup #parser
from pyvirtualdisplay import Display #simulate screen for Pepper(Pi)

import requests 

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from spidersecrets import NYU_NetID, NYU_Pass

class BeautifulSpider: 
	#netid and password can be changed from spidersecrets.py
	name = "beautifulspider"
	netid = NYU_NetID
	password = NYU_Pass
	start_url = "https://students.nyuad.nyu.edu/"

	#constructor variable defines driver and defines wait (for easy reuse)
	def __init__(self):

		print ("Initializing " + self.name + "!") #logging 
		self.display = Display(visible=0, size=(800,600)) #initialize display 
		self.display.start() #begin display

		self.driver = webdriver.Firefox() #ignition switch for selenium
		self.wait = WebDriverWait(self.driver, 10) #predefine simple wait 

	#login to shibboleth to obtain duo page
	def login (self): 

		print ("Spider is retrieving URL") #logging
		self.driver.get(self.start_url) #retrieve predefined url

		waitForm = self.wait.until(
			EC.visibility_of_element_located((By.ID,"login"))
			) #wait 10 seconds or until login form shows up

		netid = self.driver.find_element_by_xpath('//*[@id="netid"]') #find netid input space
		password = self.driver.find_element_by_xpath('//*[@id="password"]') #find password input space

		print ("Spider is logging in") #logging
		netid.send_keys(self.netid) #send netid to login form
		password.send_keys(self.password) #send password to login form

		submitButton = self.driver.find_element_by_name("_eventId_proceed") #find submit button
		submitButton.click() #click submit
		print ("Spider has logged in") #logging

	#automate phone notification; this function will eventually be updated by woswos 
	def authenticate(self):

		waitForDuo = self.wait.until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="duo_form"]'))
			) #wait until duoform shows up 

		print ("Spider has found duo") #logging

		self.driver.switch_to_frame("duo_iframe") #switch into the duo iframe

		waitforButton = self.wait.until(
			EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/fieldset[2]/div[1]/button' ))
			) #wait for the first button (push notif) to become clickable

		pushAuthButton = self.driver.find_element_by_xpath(
			'//*[@id="login-form"]/fieldset[2]/div[1]/button'
			) #find the push notif button 

		pushAuthButton.click() #click the push notif button

		print ("Spider has sent push notification") #logging

		self.driver.switch_to_default_content() #as a safety measure, switch back to parent frame

	#ensure that student portal has opened
	def waitForPortal(self):

		longerWait = WebDriverWait(self.driver, 60) #define new wait

		waitForPortal = longerWait.until(
			EC.presence_of_element_located((By.ID, 'pageTitle'))
			) #find the page title to confirm the page has loaded

	#Modular Scrape Series (MSS): Obtain Bus Schedule


	# def getBusSchedule (self):
	# 	self.driver.get(self.start_url + "/files/resources/nyuad-shuttle-schedule.pdf")
		
	# 	Download File  [Arguments]  ${COOKIE}  ${URL}  ${FILENAME}
	# 		${COOKIE_VALUE} =  Call Selenium API  get_cookie_by_name  ${COOKIE}
	# 		Run and Return RC  wget --cookies=on --header "Cookie: ${COOKIE}=${COOKIE_VALUE}" -O ${OUTPUT_DIR}${/}${FILENAME} ${URL}

		





		# r = requests.get("https://students.nyuad.nyu.edu//files/resources/nyuad-shuttle-schedule.pdf", stream = True)

		# with open("shuttle.pdf", "w") as pdf:
		# 	for chunk in r.iter_content(chunk_size)


#main function
object = BeautifulSpider()
object.login()
object.authenticate()
object.waitForPortal()
#object.getBusSchedule()






