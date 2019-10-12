
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
import math

login = 'TestKonto.0us@20mail.it'
pwd = 'testkonto'
bot = None

##############################DODAĆ initial build cost dla każdego itemu xd zeby nie trzeba bylo sprawdzac kosztu budowy w przegladarce tylko szybkie obliczenia

items = {
    'items': [{'id': '1', 'code': 'metal', 'name': 'Kopalnia metalu', 'tab': 'resources',
               'base_build_cost':{'metal': 60, 'crystal': 15, 'deuter': 0, 'energy': 0}},
              {'id': '2', 'code': 'crystal', 'name': 'Kopalnia kryształu', 'tab': 'resources',
               'base_build_cost':{'metal': 48, 'crystal': 24, 'deuter': 0, 'energy': 0}},
              {'id': '3', 'code': 'deuter', 'name': 'Ekstraktor deuteru', 'tab': 'resources',
               'base_build_cost':{'metal': 225, 'crystal': 75, 'deuter': 0, 'energy': 0}}, 
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
              {'id': '212', 'code': 'solar_sat', 'name': 'Satelita słoneczny', 'tab': 'shipyard',
               'base_build_cost':{'metal': 0, 'crystal': 2000, 'deuter': 500, 'energy': 0}},
              
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



class Bot:
    
    lobby_url = 'https://lobby.ogame.gameforge.com/pl_PL/hub'
    
    def __init__(self, login, pwd, driver):
        
        self.AccLogin = login
        self.AccPassword = pwd
        self.browser = driver 
        self.name = '???'
    
    
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
        print('DONE!')


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

   
   
driver_path = "C:\\Users\\HECki\\Documents\\Python_Scripts\\chromedriver.exe"
driver =  webdriver.Chrome(driver_path)
bot = Bot(login, pwd, driver)
bot.start()

###########################################
# TUTAJ SIE DZIEJA NOWE CUDA BEZ KLIKANIA #
###########################################

class Utils:
    @staticmethod
    def thousandSeparate(value,separator='.'):
        v = str(value)
        rv = list(reversed(v))
        for i,char in enumerate(rv):
            if not i%3 and i > 0 and i+1 != len(rv):
                rv[i] = char+separator
        v = ''.join(list(reversed(rv)))
        return v
class Resources:
    def __init__(self,metal=0,crystal=0,deuter=0,energy=0,dic=None):
        if dic:
            self.metal = dic['metal']
            self.crystal = dic['crystal']
            self.deuter = dic['deuter']
            self.energy = dic['energy']
        else:
            self.metal = metal
            self.crystal = crystal
            self.deuter = deuter
            self.energy = energy
        self.formatAttributes()
        
        
    def formatAttributes(self):
        #_f = formatted
        self.metal_f = Utils.thousandSeparate(self.metal)
        self.crystal_f = Utils.thousandSeparate(self.crystal)
        self.deuter_f = Utils.thousandSeparate(self.deuter)
        self.energy_f = Utils.thousandSeparate(self.energy)
        
    
    def isNegative(self):
        negatives = self.__dict__()
        to_pop = []
        for v in negatives.items():
            if v[1] >= 0:
                to_pop.append(v[0])
        for key in to_pop:
        	negatives.pop(key,None)

        if len(negatives) == 0:
            return False
        return negatives
        
        
    def __add__(self,other):   
        if isinstance(other,Resources):
            metal = self.metal + other.metal
            crystal = self.crystal + other.crystal
            deuter = self.deuter + other.deuter
            energy = self.energy + other.energy
        return Resources(metal,crystal,deuter,energy)
    
    
    def __sub__(self,other):   
        if isinstance(other,Resources):
            metal = self.metal - other.metal
            crystal = self.crystal - other.crystal
            deuter = self.deuter - other.deuter
            energy = self.energy - other.energy
        return Resources(metal,crystal,deuter,energy)
    
    
    def __mul__(self,other):
        metal = math.floor(self.metal * other)
        crystal = math.floor(self.crystal * other)
        deuter = math.floor(self.deuter * other)
        energy = math.floor(self.energy * other)
        return Resources(metal,crystal,deuter,energy)
    
    def __dict__(self):
        d = {}
        d['metal'] = self.metal
        d['crystal'] = self.crystal
        d['deuter'] = self.deuter
        d['energy'] = self.energy
        return d
    
        
    def __str__(self):
        return f'Metal: {self.metal}  Kryształ: {self.crystal}  Deuter: {self.deuter}  Energia: {self.energy}'


class Tab:
    
    tab_codes = ['resources','station','research','shipyard','defense']
    tabs = {}
    base_url = 'https://s163-pl.ogame.gameforge.com/game/index.php?page='
    
    
    def __init__(self,code):
        
        self.code = code
        self.url = Tab.base_url + code
        
        if code == 'research':
            self.content_class = 'wrapButtons'
        else:
            self.content_class = 'content'
            
        self.items = []
        self.token = None
        
        
    def open(self):
        if Tab.getCurrentTab() == self:
            self.findToken()
            return
        bot.browser.get(self.url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "info")))
        self.findToken(bot.browser.page_source)


    def findToken(self,code):
        
        if self.code in ('research','shipyard'):
            return None
        bs = BeautifulSoup(code,features="html.parser")
        a = bs.find('a',{'class':'fastBuild tooltip js_hideTipOnMobile'})
        if a is None:
            return None
        else:
            tokens = a.get('onclick').split('token=')
            try:
                token = tokens[1][:32]
            except:
                return None
        self.token = token
        return token


    def getRequestLink(self,type):
        
        self.open()
        url = f'https://s163-pl.ogame.gameforge.com/game/index.php?page={self.code}&modus=1&menge=1&type={type}'
        if self.token:
            url += "&token=" + self.token
        return url

    '''
    
    Funkcja na potrzebe zapisania wszystkiego do listy 'items'
    
    def getInfo(self):
        
        bs = BeautifulSoup(bot.browser.page_source,features="html.parser")
        content = bs.find('div',{'class':self.content_class})
        d = {'items':[]}
        
        for li in content.findAll('li'):
            id = '?'
            for a in li.findAll('a'):
                if a.get('ref'):
                    id = a.get('ref')
                    break
            text_label = li.find('span',{'class':'level'})
            
            t = text_label.getText()
            rt = re.sub('\s+',' ',t)
            if rt[0] in ('\n','\t','\s',' '):
                rt = rt[1:]
            rt = rt.lstrip().rstrip()
            split = rt.split(' ')
            level = split[-1]
            name = ' '.join(split[:-1])
            d['items'].append({'id':id, 'name':name, 'tab':self.code})
            #print(f'({id}) ' + name + ": " + level)
        print(d)
    '''
        
    def update(self):
        self.findToken(bot.browser.page_source)
        
        bs = BeautifulSoup(bot.browser.page_source,features="html.parser")
        content = bs.find('div',{'class':self.content_class})
        
        for li in content.findAll('li'):
            id = 0
            for a in li.findAll('a'):
                if a.get('ref'):
                    id = a.get('ref')
                    break
                
            item = Buildable.getItem(id,by='id')
            
            text_label = li.find('span',{'class':'level'})

            t = text_label.getText()
            rt = re.sub('\s+',' ',t)
            if rt[0] in ('\n','\t','\s',' '):
                rt = rt[1:]
                
            rt = rt.lstrip().rstrip()
            split = rt.split(' ')
            
            item.level = int(split[-1])     
      
      
    def __str__(self):
        t = f'[{self.code.upper()}] TOKEN: {self.token}\n\n[ITEMS]\n'
        for item in Buildable.buildables:
            if item.tab == self:
                t += str(item) + "\n"
        return t
    
    
    @classmethod
    def getCurrentTab(cls):
        
        for tab in cls.tab_codes:
            if bot.browser.current_url.endswith(tab):
                return cls.tabs[tab]
        return None


    @classmethod
    def initialize(cls):
        
        print('Initializing tabs')
        for tc in cls.tab_codes:
            print(f'Creating {tc}')
            cls.tabs[tc] = cls(tc)
        print("DONE")


        
class Buildable:
    buildables = []

    def __init__(self,d):
        self.id = d['id']
        self.code = d['code']
        self.name = d['name']
        self.tab = Tab.tabs[d['tab']]
        self.tab.items.append(self)
        self.base_build_cost = Resources(dic=d['base_build_cost'])#to tu jest tylko dla testów
        self.level = -1 #to tu jest tylko dla testów
        
    def build(self):
        
        build_link = self.tab.getRequestLink(self.type)
        #print(f'BL: {build_link}')
        #bot.browser.get(build_link)
        bot.browser.execute_script(f"sendBuildRequest('{build_link}', null, 1);")
        
        
    def getBuildCost(self,level=None):
        
        if level is None:
            level = self.level+1
        else:
            level = level

        base_cost = self.base_build_cost
        multiplier = self.getCostMultiplier()
        
        return base_cost * (multiplier ** (level-1))
            
    
    
    def __str__(self):
        #return f'({self.id}#{self.code}) {self.name}: {self.level} Lvl'   
        return f'{self.name}: {self.level} Lvl [UPGRADE] {self.getBuildCost()}'  
        
    
    def getCostMultiplier(self):
        
        bcm = {'metal':1.5,'solar':1.5,'deuter':1.5,'crystal':1.6,'fusion':1.8,'other':2.0}
        if self.code in bcm.keys():
            return bcm[self.code]
        
        return bcm['other']
        
        
    @classmethod
    def initialize(cls):
        
        for item in items['items']:
            cls.buildables.append(Buildable(item))

    @classmethod
    def getItem(cls,value,by='id'):
        
        for item in cls.buildables:
            if getattr(item,by) == value:
                return item
        
        return None


Tab.initialize()
Buildable.initialize()
#Buildable.buildings['satelite'].build()


while True:
    
    time.sleep(0.5)
    os.system('cls')
    t = Tab.getCurrentTab()
    token = None
    if t:
        t.update()
        print(t)
    else:
        print('Unknown tab')
 
