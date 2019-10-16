
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time 
import os
import pyperclip
from datetime import datetime
from bs4 import BeautifulSoup
import random
import re
import json



login = 'TestKonto.0us@20mail.it'
pwd = 'testkonto'
bot = None


from resources import Resources
from utils import *
from buildable_tab import Tab, Buildable
from bot_instance import BI

    
class Bot:
    lobby_url = 'https://lobby.ogame.gameforge.com/pl_PL/hub'
    
    def __init__(self, login, pwd, driver):
        BI.bot = self
        self.AccLogin = login
        self.AccPassword = pwd
        self.browser = driver 
        self.name = '???'

        self.resources = Resources()
        self.text_output = []
        
    def login(self):
        
        self.browser.get(Bot.lobby_url)
        #Znalezienie przycisku zakładki Login
        login_button = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/ul/li[1]')
        login_button.click()
        #Input loginu i hasła
        login_text_field = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/form/div[1]/div/input')
        login_text_field.send_keys(self.AccLogin)
        pwd_text_field = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/form/div[2]/div/input')
        pwd_text_field.send_keys(self.AccPassword)
        #Klik login
        login_button = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/form/p/button[1]')
        login_button.click()


    def log(self):
        
        play_button = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/a')
        play_button.click()


    def temp(self):
        
        kalyke_start_button = self.find(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/section[1]/div[2]/div/div/div[1]/div[2]/div/div/div[11]/button')
        kalyke_start_button.click()


    def start(self):
        
        print('Logging in...')
        self.login()
        self.log()
        print('Entering universe...')
        self.temp()
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.find(By.ID, "resources")
        self.name = self.find(By.XPATH,'/html/body/div[2]/div[2]/div/div[1]/div[5]/ul/li[1]/span/a',attr='text')
        print('Logged in.')
        self.initialize()

    def initialize(self):

        Tab.initialize()
        Buildable.initialize()
        #Tab.updateAll()


    def find(self,by,value,attr=None,conv=None,preconv=None,postconv=None,timer=10,no_wait=False):
        
        if no_wait:
            element = self.browser.find_element(by=by,value=value)
        else:
            try:
                element = WebDriverWait(self.browser, timer).until(EC.presence_of_element_located((by, value)))
            except:
                print(f"! COULDNT FIND ELEMENT\n{value}\nby {by}")
                return
        if attr:
            element = getattr(element,attr)
        if preconv:
            element = preconv(element)
        if conv:
            element = conv(element)
        if postconv:
            element = postconv(element)
        return element

    def updateResources(self):
        
        bs = BeautifulSoup(bot.browser.page_source,features="html.parser")
        metal = bs.find('span',{'id':'resources_metal'}).getText()
        crystal = bs.find('span',{'id':'resources_crystal'}).getText()
        deuter = bs.find('span',{'id':'resources_deuterium'}).getText()
        energy = bs.find('span',{'id':'resources_energy'}).getText()
        
        self.resources = Resources(metal,crystal,deuter,energy)


    def add_output(self,v):
        self.text_output.append(str(v))
    
    
    def clear_output(self):
        self.text_output = []
    
    
    def print_output(self):
        print("\n".join(self.text_output))
    

    def tick(self):
        self.updateResources()
        self.add_output(self)
        ct = Tab.getCurrentTab()
        if isinstance(ct,Tab):
            ct.update()
        
        self.add_output(ct)
        bi = Buildable.getBuildableItems()
        
    
    def __str__(self):
        return f'[BOT]\n[RESOURCES] {self.resources}'
   
   
driver_path = "C:\\webdrivers\\chromedriver.exe"
driver =  webdriver.Chrome(driver_path)
bot = Bot(login, pwd, driver)
bot.start()

update_interval = 0.1


bot.tick()
Buildable.getItem('mt',by='code').build(2)

#Tab.tabs['shipyard'].open()
#bot.browser.execute_script("document.getElementsByClassName('detail_screen')[0].innerHTML='{replacementHTML}'")

while True:
    
    
    bot.tick()
    os.system('cls')
    bot.print_output()
    bot.clear_output()

    time.sleep(update_interval)
