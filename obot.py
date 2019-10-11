
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




items = {
    'items': [{'id': '1', 'name': 'Kopalnia metalu', 'tab': 'resources'}, 
              {'id': '2', 'name': 'Kopalnia kryształu', 'tab': 'resources'}, 
              {'id': '3', 'name': 'Ekstraktor deuteru', 'tab': 'resources'}, 
              {'id': '4', 'name': 'Elektrownia słoneczna', 'tab': 'resources'}, 
              {'id': '12', 'name': 'Elektrownia fuzyjna', 'tab': 'resources'}, 
              {'id': '212', 'name': 'Satelita słoneczny', 'tab': 'resources'}, 
              {'id': '22', 'name': 'Magazyn metalu', 'tab': 'resources'}, 
              {'id': '23', 'name': 'Magazyn kryształu', 'tab': 'resources'}, 
              {'id': '24', 'name': 'Zbiornik deuteru', 'tab': 'resources'},
              {'id': '14', 'name': 'Fabryka robotów', 'tab': 'station'}, 
              {'id': '21', 'name': 'Stocznia', 'tab': 'station'}, 
              {'id': '31', 'name': 'Laboratorium badawcze', 'tab': 'station'}, 
              {'id': '34', 'name': 'Depozyt sojuszniczy', 'tab': 'station'}, 
              {'id': '44', 'name': 'Silos rakietowy', 'tab': 'station'}, 
              {'id': '15', 'name': 'Fabryka nanitów', 'tab': 'station'}, 
              {'id': '33', 'name': 'Terraformer', 'tab': 'station'}, 
              {'id': '36', 'name': 'Dok kosmiczny', 'tab': 'station'},
              {'id': '113', 'name': 'Technologia energetyczna', 'tab': 'research'},
              {'id': '120', 'name': 'Technologia laserowa', 'tab': 'research'}, 
              {'id': '121', 'name': 'Technologia jonowa', 'tab': 'research'}, 
              {'id': '114', 'name': 'Technologia nadprzestrzenna', 'tab': 'research'}, 
              {'id': '122', 'name': 'Technologia plazmowa', 'tab': 'research'}, 
              {'id': '115', 'name': 'Napęd spalinowy', 'tab': 'research'},
              {'id': '117', 'name': 'Napęd impulsowy', 'tab': 'research'},
              {'id': '118', 'name': 'Napęd nadprzestrzenny', 'tab': 'research'}, 
              {'id': '106', 'name': 'Technologia szpiegowska', 'tab': 'research'}, 
              {'id': '108', 'name': 'Technologia komputerowa', 'tab': 'research'}, 
              {'id': '124', 'name': 'Astrofizyka', 'tab': 'research'}, 
              {'id': '123', 'name': 'Międzygalaktyczna Sieć Badań Naukowych', 'tab': 'research'}, 
              {'id': '199', 'name': 'Rozwój grawitonów', 'tab': 'research'}, 
              {'id': '109', 'name': 'Technologia bojowa', 'tab': 'research'}, 
              {'id': '110', 'name': 'Technologia ochronna', 'tab': 'research'}, 
              {'id': '111', 'name': 'Opancerzenie', 'tab': 'research'}, 
              {'id': '204', 'name': 'Lekki myśliwiec', 'tab': 'shipyard'}, 
              {'id': '205', 'name': 'Ciężki myśliwiec', 'tab': 'shipyard'}, 
              {'id': '206', 'name': 'Krążownik', 'tab': 'shipyard'}, 
              {'id': '207', 'name': 'Okręt wojenny', 'tab': 'shipyard'}, 
              {'id': '215', 'name': 'Pancernik', 'tab': 'shipyard'}, 
              {'id': '211', 'name': 'Bombowiec', 'tab': 'shipyard'}, 
              {'id': '213', 'name': 'Niszczyciel', 'tab': 'shipyard'}, 
              {'id': '214', 'name': 'Gwiazda Śmierci', 'tab': 'shipyard'}, 
              {'id': '202', 'name': 'Mały transporter', 'tab': 'shipyard'}, 
              {'id': '203', 'name': 'Duży transporter', 'tab': 'shipyard'}, 
              {'id': '208', 'name': 'Statek kolonizacyjny', 'tab': 'shipyard'}, 
              {'id': '209', 'name': 'Recykler', 'tab': 'shipyard'}, 
              {'id': '210', 'name': 'Sonda szpiegowska', 'tab': 'shipyard'}, 
              {'id': '212', 'name': 'Satelita słoneczny', 'tab': 'shipyard'},
              {'id': '401', 'name': 'Wyrzutnia rakiet', 'tab': 'defense'}, 
              {'id': '402', 'name': 'Lekkie działo laserowe', 'tab': 'defense'}, 
              {'id': '403', 'name': 'Ciężkie działo laserowe', 'tab': 'defense'}, 
              {'id': '404', 'name': 'Działo Gaussa', 'tab': 'defense'}, 
              {'id': '405', 'name': 'Działo jonowe', 'tab': 'defense'}, 
              {'id': '406', 'name': 'Wyrzutnia plazmy', 'tab': 'defense'}, 
              {'id': '407', 'name': 'Mała powłoka ochronna', 'tab': 'defense'}, 
              {'id': '408', 'name': 'Duża powłoka ochronna', 'tab': 'defense'}, 
              {'id': '502', 'name': 'Przeciwrakieta', 'tab': 'defense'}, 
              {'id': '503', 'name': 'Rakieta międzyplanetarna', 'tab': 'defense'}]
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
        bot.browser.get(self.url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "info")))
        self.token = self.findToken(bot.browser.page_source)

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
        return token
        '''
        else:
            bs = BeautifulSoup(code,features="html.parser")
            a = bs.find('input',{'name':'token'})
            if a is None:
                return None
            else:
                token = a.get('value')
            return token
        '''
    def getRequestLink(self,type):
        self.open()
        url = f'https://s163-pl.ogame.gameforge.com/game/index.php?page={self.code}&modus=1&menge=1&type={type}'
        if self.token:
            url += "&token=" + self.token
        return url

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

class Building:
    buildings = []
    @classmethod
    def do(self,id,name,level,tab):
        
        for b in Building.buildings:
            if b.id == id:
                b.upate(level)
                return
        Building(id,name,level)
        
    def __init__(self,id,name,level,tab):
        self.id = id
        self.name = name
        self.level = level
        self.tab = Tab.tabs[tab]
        Building.buildings.append(self)
        
    def uptate(self,level):
        self.level = level
    
class ItemHandle:
    building_codes = [
        ('metal','resources',1),
        ('crystal','resources',2),
        ('deuter','resources',3),
        ('solar','resources',4),
        ('satelite','resources',212),
        ('metal_depo','resources',22),
        ('crystal_depo','resources',23),
        ('metal_depo','resources',24),
        ('robot_factory','station',14),
        ('shipyard','station',21),
        ('lab','station',31),
        ('nanit','station',15),
        ('light_fighter','shipyard',204)
        ]
    
    research_codes = [
        ('energetic','research',113),
        ('laser','research',120),
        ('ion','research',121),
        ('hyperspace_tech','research',114),
        ('plasma','research',122),
        ('combustion','research',115),
        ('impulse','research',117),
        ('hyperspace','research',118),
        ('espionage','research',106),
        ('computer','research',108),
        ('astro','research',124),
        ('research_network','research',123),
        ('graviton','research',199),
        ('weapon','research',109),
        ('shield','research',110),
        ('armor','research',111),
    ]


    buildings = {}
    researches = {}
    def __init__(self,tup):
        self.name = tup[0]
        self.type = tup[2]
        self.tab = Tab.tabs[tup[1]]
    def build(self):
        build_link = self.tab.getRequestLink(self.type)
        print(f'BL: {build_link}')
        #bot.browser.get(build_link)
        bot.browser.execute_script(f"sendBuildRequest('{build_link}', null, 1);")
    @classmethod
    def initialize(cls):
        for bc in cls.building_codes:
            cls.buildings[bc[0]] = cls(bc)
        for rc in cls.research_codes:
            cls.researches[rc[0]] = cls(rc)

Tab.initialize()
ItemHandle.initialize()

#ItemHandle.buildings['satelite'].build()


while True:
    time.sleep(0.5)
    os.system('cls')
    t = Tab.getCurrentTab()
    token = None
    if t:
        token = t.findToken(bot.browser.page_source)
        print(f"{t.code} TOKEN: {token}")
        t.getInfo()
    else:
        print('Unknown tab')
 
