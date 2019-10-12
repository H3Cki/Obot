from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from resources import Resources
import json
import re
from selenium.webdriver.support import expected_conditions as EC
import time 

with open('items.txt', 'r') as f:
    items = json.load(f)

bot = None

class BotInitializer:
    @classmethod
    def initialize_bot(cls,_bot):
        global bot
        bot = _bot



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
        element = WebDriverWait(bot.browser, 10).until(EC.presence_of_element_located((By.ID, "info")))
        self.findToken()


    def findToken(self,code=None):
        code = bot.browser.page_source or code
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
        self.findToken()
        
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
        tab_url = bot.browser.current_url.split('page=')[-1].split('&')[0]
        for tab in cls.tab_codes:
            if tab_url.endswith(tab):
                return cls.tabs[tab]
        return f"Zakładka '{tab_url}' nie jest obsługiwana"


    @classmethod
    def initialize(cls):
        print('Initializing tabs')
        for tc in cls.tab_codes:
            print(f'Creating {tc}')
            cls.tabs[tc] = cls(tc)
        print("DONE")
        
        

class Buildable(BotInitializer):
    buildables = []

    def __init__(self,d):
        self.id = d['id']
        self.code = d['code']
        self.name = d['name']
        self.tab = Tab.tabs[d['tab']]
        self.tab.items.append(self)
        self.base_build_cost = Resources(dic=d['base_build_cost'])#to tu jest tylko dla testów
        self.level = -1 #to tu jest tylko dla testów
        
    def build(self,n=1):

        build_link = self.tab.getRequestLink(self.id)
        #print(f'BL: {build_link}')
        #bot.browser.get(build_link)
        if self.tab.code in ['resources','station','research']:
            bot.browser.execute_script(f"sendBuildRequest('{build_link}', null, 1);")
        else:
            el = bot.browser.find_element_by_id('details'+self.id)
            el.click()
            #bot.browser.find_element_by_id('number').SetAttribute("value", 2);
            try:
                WebDriverWait(bot.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "build-it")))
            except:
                return
            bot.browser.execute_script(f"checkIntInput(null, {n}, 99999);")
            bot.browser.execute_script(f"sendBuildRequest(null, event, false);")
        
        
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