
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
from buildable_tab import *

##############################DODAĆ initial build cost dla każdego itemu xd zeby nie trzeba bylo sprawdzac kosztu budowy w przegladarce tylko szybkie obliczenia
'''
items = {
    'items': [{'id': '1', 'code': 'metal', 'name': 'Kopalnia metalu', 'tab': 'resources',
               'base_build_cost':{'metal': 60, 'crystal': 15, 'deuter': 0, 'energy': 11}},
              {'id': '2', 'code': 'crystal', 'name': 'Kopalnia kryształu', 'tab': 'resources',
               'base_build_cost':{'metal': 48, 'crystal': 24, 'deuter': 0, 'energy': 11}},
              {'id': '3', 'code': 'deuter', 'name': 'Ekstraktor deuteru', 'tab': 'resources',
               'base_build_cost':{'metal': 225, 'crystal': 75, 'deuter': 0, 'energy': 22}}, 
              {'id': '4', 'code': 'solar', 'name': 'Elektrownia słoneczna', 'tab': 'resources',
               'base_build_cost':{'metal': 75, 'crystal': 30, 'deuter': 0, 'energy': 0}}, 
              {'id': '12', 'code': 'fusion', 'name': 'Elektrownia fuzyjna', 'tab': 'resources',
               'base_build_cost':{'metal': 900, 'crystal': 360, 'deuter': 180, 'energy': 0}}, 
              {'id': '212', 'code': 'solar_sat', 'name': 'Satelita słoneczny', 'tab': 'resources',
               'base_build_cost':{'metal': 0, 'crystal': 2000, 'deuter': 500, 'energy': 0}}, 
              {'id': '22', 'code': 'metal_depo', 'name': 'Magazyn metalu', 'tab': 'resources',
               'base_build_cost':{'metal': 1000, 'crystal': 0, 'deuter': 0, 'energy': 0}}, 
              {'id': '23', 'code': 'crystal_depo', 'name': 'Magazyn kryształu', 'tab': 'resources',
               'base_build_cost':{'metal': 1000, 'crystal': 500, 'deuter': 0, 'energy': 0}}, 
              {'id': '24', 'code': 'deuter_depo', 'name': 'Zbiornik deuteru', 'tab': 'resources',
               'base_build_cost':{'metal': 1000, 'crystal': 1000, 'deuter': 0, 'energy': 0}},
              
              {'id': '14', 'code': 'robot', 'name': 'Fabryka robotów', 'tab': 'station',
               'base_build_cost':{'metal': 400, 'crystal': 120, 'deuter': 200, 'energy': 0}}, 
              {'id': '21', 'code': 'shipyard', 'name': 'Stocznia', 'tab': 'station',
               'base_build_cost':{'metal': 400, 'crystal': 200, 'deuter': 100, 'energy': 0}}, 
              {'id': '31', 'code': 'lab', 'name': 'Laboratorium badawcze', 'tab': 'station',
               'base_build_cost':{'metal': 200, 'crystal': 400, 'deuter': 200, 'energy': 0}}, 
              {'id': '34', 'code': 'depo', 'name': 'Depozyt sojuszniczy', 'tab': 'station',
               'base_build_cost':{'metal': 20000, 'crystal': 40000, 'deuter': 0, 'energy': 0}}, 
              {'id': '44', 'code': 'silo', 'name': 'Silos rakietowy', 'tab': 'station',
               'base_build_cost':{'metal': 20000, 'crystal': 20000, 'deuter': 1000, 'energy': 0}}, 
              {'id': '15', 'code': 'nanit', 'name': 'Fabryka nanitów', 'tab': 'station',
               'base_build_cost':{'metal': 1000000, 'crystal': 500000, 'deuter': 100000, 'energy': 0}},
              {'id': '33', 'code': 'terra', 'name': 'Terraformer', 'tab': 'station',
               'base_build_cost':{'metal': 0, 'crystal': 50000, 'deuter': 100000, 'energy': 0}}, 
              {'id': '36', 'code': 'dok', 'name': 'Dok kosmiczny', 'tab': 'station',
               'base_build_cost':{'metal': 200, 'crystal': 0, 'deuter': 50, 'energy': 0}},
              
              {'id': '113', 'code': 'energetic', 'name': 'Technologia energetyczna', 'tab': 'research',
               'base_build_cost':{'metal': 0, 'crystal': 800, 'deuter': 400, 'energy': 0}},
              {'id': '120', 'code': 'laser', 'name': 'Technologia laserowa', 'tab': 'research',
               'base_build_cost':{'metal':2000, 'crystal': 100, 'deuter': 0, 'energy': 0}}, 
              {'id': '121', 'code': 'ion', 'name': 'Technologia jonowa', 'tab': 'research',
               'base_build_cost':{'metal': 1000, 'crystal': 300, 'deuter': 100, 'energy': 0}}, 
              {'id': '114', 'code': 'hyperspace_tech', 'name': 'Technologia nadprzestrzenna', 'tab': 'research',
               'base_build_cost':{'metal': 0, 'crystal': 4000, 'deuter': 2000, 'energy': 0}}, 
              {'id': '122', 'code': 'plasma', 'name': 'Technologia plazmowa', 'tab': 'research',
               'base_build_cost':{'metal': 2000, 'crystal': 4000, 'deuter': 1000, 'energy': 0}}, 
              {'id': '115', 'code': 'combustion', 'name': 'Napęd spalinowy', 'tab': 'research',
               'base_build_cost':{'metal': 400, 'crystal': 0, 'deuter': 600, 'energy': 0}},
              {'id': '117', 'code': 'impulse', 'name': 'Napęd impulsowy', 'tab': 'research',
               'base_build_cost':{'metal': 2000, 'crystal': 4000, 'deuter': 600, 'energy': 0}},
              {'id': '118', 'code': 'hyperspace', 'name': 'Napęd nadprzestrzenny', 'tab': 'research',
               'base_build_cost':{'metal': 10000, 'crystal': 20000, 'deuter': 6000, 'energy': 0}}, 
              {'id': '106', 'code': 'espionage', 'name': 'Technologia szpiegowska', 'tab': 'research',
               'base_build_cost':{'metal': 200, 'crystal': 1000, 'deuter': 200, 'energy': 0}}, 
              {'id': '108', 'code': 'computer', 'name': 'Technologia komputerowa', 'tab': 'research',
               'base_build_cost':{'metal': 0, 'crystal': 400, 'deuter': 600, 'energy': 0}}, 
              {'id': '124', 'code': 'astro', 'name': 'Astrofizyka', 'tab': 'research',
               'base_build_cost':{'metal': 4000, 'crystal': 8000, 'deuter': 4000, 'energy': 0}}, 
              {'id': '123', 'code': 'network', 'name': 'Międzygalaktyczna Sieć Badań Naukowych', 'tab': 'research',
               'base_build_cost':{'metal': 240000, 'crystal': 400000, 'deuter': 160000, 'energy': 0}}, 
              {'id': '199', 'code': 'graviton', 'name': 'Rozwój grawitonów', 'tab': 'research',
               'base_build_cost':{'metal': 0, 'crystal': 0, 'deuter': 0, 'energy': 300000}}, 
              {'id': '109', 'code': 'weapon', 'name': 'Technologia bojowa', 'tab': 'research',
               'base_build_cost':{'metal': 800, 'crystal': 200, 'deuter': 0, 'energy': 0}}, 
              {'id': '110', 'code': 'shield', 'name': 'Technologia ochronna', 'tab': 'research',
               'base_build_cost':{'metal': 200, 'crystal': 600, 'deuter': 0, 'energy': 0}}, 
              {'id': '111', 'code': 'armor', 'name': 'Opancerzenie', 'tab': 'research',
               'base_build_cost':{'metal': 1000, 'crystal': 0, 'deuter': 0, 'energy': 0}}, 
              
              {'id': '204', 'code': 'lm', 'name': 'Lekki myśliwiec', 'tab': 'shipyard',
               'base_build_cost':{'metal': 3000, 'crystal': 1000, 'deuter': 0, 'energy': 0}}, 
              {'id': '205', 'code': 'cm', 'name': 'Ciężki myśliwiec', 'tab': 'shipyard',
               'base_build_cost':{'metal': 6000, 'crystal': 4000, 'deuter': 0, 'energy': 0}}, 
              {'id': '206', 'code': 'kr', 'name': 'Krążownik', 'tab': 'shipyard',
               'base_build_cost':{'metal': 20000, 'crystal': 7000, 'deuter': 2000, 'energy': 0}}, 
              {'id': '207', 'code': 'ow', 'name': 'Okręt wojenny', 'tab': 'shipyard',
               'base_build_cost':{'metal': 45000, 'crystal': 15000, 'deuter': 0, 'energy': 0}}, 
              {'id': '215', 'code': 'p', 'name': 'Pancernik', 'tab': 'shipyard',
               'base_build_cost':{'metal': 30000, 'crystal': 40000, 'deuter': 15000, 'energy': 0}}, 
              {'id': '211', 'code': 'b', 'name': 'Bombowiec', 'tab': 'shipyard',
               'base_build_cost':{'metal': 50000, 'crystal': 25000, 'deuter': 15000, 'energy': 0}}, 
              {'id': '213', 'code': 'nc', 'name': 'Niszczyciel', 'tab': 'shipyard',
               'base_build_cost':{'metal': 60000, 'crystal': 50000, 'deuter': 15000, 'energy': 0}}, 
              {'id': '214', 'code': 'gs', 'name': 'Gwiazda Śmierci', 'tab': 'shipyard',
               'base_build_cost':{'metal': 5000000, 'crystal': 4000000, 'deuter': 1000000, 'energy': 0}}, 
              {'id': '202', 'code': 'mt', 'name': 'Mały transporter', 'tab': 'shipyard',
               'base_build_cost':{'metal': 2000, 'crystal': 2000, 'deuter': 0, 'energy': 0}}, 
              {'id': '203', 'code': 'dt', 'name': 'Duży transporter', 'tab': 'shipyard',
               'base_build_cost':{'metal': 6000, 'crystal': 6000, 'deuter': 0, 'energy': 0}}, 
              {'id': '208', 'code': 'kolo', 'name': 'Statek kolonizacyjny', 'tab': 'shipyard',
               'base_build_cost':{'metal': 1000, 'crystal': 20000, 'deuter': 10000, 'energy': 0}}, 
              {'id': '209', 'code': 'rec', 'name': 'Recykler', 'tab': 'shipyard',
               'base_build_cost':{'metal': 10000, 'crystal': 6000, 'deuter': 2000, 'energy': 0}}, 
              {'id': '210', 'code': 'sonda', 'name': 'Sonda szpiegowska', 'tab': 'shipyard',
               'base_build_cost':{'metal': 0, 'crystal': 1000, 'deuter': 0, 'energy': 0}}, 
              
              {'id': '401', 'code': 'wr', 'name': 'Wyrzutnia rakiet', 'tab': 'defense',
               'base_build_cost':{'metal': 2000, 'crystal': 0, 'deuter': 0, 'energy': 0}}, 
              {'id': '402', 'code': 'ldl', 'name': 'Lekkie działo laserowe', 'tab': 'defense',
               'base_build_cost':{'metal': 1500, 'crystal': 500, 'deuter': 0, 'energy': 0}}, 
              {'id': '403', 'code': 'cdl', 'name': 'Ciężkie działo laserowe', 'tab': 'defense',
               'base_build_cost':{'metal': 6000, 'crystal': 2000, 'deuter': 0, 'energy': 0}}, 
              {'id': '404', 'code': 'dg', 'name': 'Działo Gaussa', 'tab': 'defense',
               'base_build_cost':{'metal': 20000, 'crystal': 15000, 'deuter': 2000, 'energy': 0}}, 
              {'id': '405', 'code': 'dj', 'name': 'Działo jonowe', 'tab': 'defense',
               'base_build_cost':{'metal': 2000, 'crystal': 6000, 'deuter': 0, 'energy': 0}}, 
              {'id': '406', 'code': 'wp', 'name': 'Wyrzutnia plazmy', 'tab': 'defense',
               'base_build_cost':{'metal': 50000, 'crystal': 50000, 'deuter': 30000, 'energy': 0}}, 
              {'id': '407', 'code': 'mpo', 'name': 'Mała powłoka ochronna', 'tab': 'defense',
               'base_build_cost':{'metal': 10000, 'crystal': 10000, 'deuter': 0, 'energy': 0}}, 
              {'id': '408', 'code': 'dpo', 'name': 'Duża powłoka ochronna', 'tab': 'defense',
               'base_build_cost':{'metal': 50000, 'crystal': 50000, 'deuter': 0, 'energy': 0}}, 
              {'id': '502', 'code': 'anti_rocket', 'name': 'Przeciwrakieta', 'tab': 'defense',
               'base_build_cost':{'metal': 8000, 'crystal': 2000, 'deuter': 0, 'energy': 0}}, 
              {'id': '503', 'code': 'rocket', 'name': 'Rakieta międzyplanetarna', 'tab': 'defense',
               'base_build_cost':{'metal': 12500, 'crystal': 2500, 'deuter': 10000, 'energy': 0}}]
}
'''

class Bot:
    
    lobby_url = 'https://lobby.ogame.gameforge.com/pl_PL/hub'
    
    def __init__(self, login, pwd, driver):
        
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
        
        BotInitializer.initialize_bot(self)
        Tab.initialize()
        Buildable.initialize()
        Tab.updateAll()
        print("READY!")


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
   
   
driver_path = "C:\\Users\\HECki\\Documents\\Python_Scripts\\chromedriver.exe"
driver =  webdriver.Chrome(driver_path)
bot = Bot(login, pwd, driver)
bot.start()

update_interval = 0.1


while True:
    
    
    bot.tick()
    os.system('cls')
    bot.print_output()
    bot.clear_output()

    time.sleep(update_interval)
