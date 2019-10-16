from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from resources import Resources
import json
import re
from selenium.webdriver.support import expected_conditions as EC
import time 
from bot_instance import BI

with open('items.txt', 'r') as f:
    items = json.load(f)

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
        BI.bot.browser.get(self.url)
        element = WebDriverWait(BI.bot.browser, 10).until(EC.presence_of_element_located((By.ID, "info")))
        self.findToken()


    def findToken(self,code=None):
        code = BI.bot.browser.page_source or code
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
        
        bs = BeautifulSoup(BI.bot.browser.page_source,features="html.parser")
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
        
    def update(self,open=False):
        if Tab.getCurrentTab() != self:
            if open:
                self.open()
            else: return
        self.findToken()
        
        bs = BeautifulSoup(BI.bot.browser.page_source,features="html.parser")
        content = bs.find('div',{'class':self.content_class})
        
      
        for li in content.findAll('li'):
            id = 0
            for a in li.findAll('a'):
                if a.get('ref'):
                    id = a.get('ref')
                    break
                
            item = Buildable.getItem(id,by='id')
            
            if not item: return
            
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
        tab_url = BI.bot.browser.current_url.split('page=')[-1].split('&')[0]
        for tab in cls.tab_codes:
            if tab_url.endswith(tab):
                return cls.tabs[tab]
        return f"Zakładka '{tab_url}' nie jest obsługiwana"


    @classmethod
    def initialize(cls):
        print('Initializing tabs')
        for tc in Tab.tab_codes:
            print(f'Creating {tc}')
            Tab.tabs[tc] = cls(tc)
        print("DONE")
        
        
    @classmethod
    def updateAll(cls):
        print("Updating all tabs...")
        for t in Tab.tabs.items():
            print(t[1].code)
            t[1].update(open=True)
        print("DONE")

        
class Buildable:
    buildables = []

    def __init__(self,d):
        self.id = d['id']
        self.code = d['code']
        self.name = d['name']
        self.tab = Tab.tabs[d['tab']]
        self.tab.items.append(self)
        self.base_build_cost = Resources(dic=d['base_build_cost'])
        self.tab.update() #to tu jest tylko dla testów
        self.level = -1

        
    def canBuild(self):
        balance = BI.bot.resources.pay(self.getBuildCost(),skip_energy = self.getBuildCost().energy <= 0)
        return balance.isPositive()
    
    
    def build(self,n=1):
 
        self.tab.update(open=True)

        if not self.canBuild():
            return False

        #BI.bot.browser.get(build_link)
        if self.tab.code in ['resources','station','research']:
            build_link = self.tab.getRequestLink(self.id)
            BI.bot.browser.execute_script(f"sendBuildRequest('{build_link}', null, 1);")
        else:
            #STARY KOD
            '''
            el = BI.bot.browser.find_element_by_id('details'+self.id)
            el.click()
            #BI.bot.browser.find_element_by_id('number').SetAttribute("value", 2);
            try:
                WebDriverWait(BI.bot.browser, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "build-it")))
            except:
                return False
            BI.bot.browser.execute_script(f"checkIntInput(null, {n}, 99999);")
            BI.bot.browser.execute_script(f"sendBuildRequest(null, event, false);")
            '''
            
            
            
            
            replacementHTML = []
            replacementHTML.append(f'<input type="hidden" name="modus" value="1"></input>')
            replacementHTML.append(f'<input type="hidden" name="type" value={self.id}></input>')
            replacementHTML.append(f'<input id="number" type="text" class="amount_input" pattern="[0-9,.]*" size="5" name="menge" value={n} onfocus="clearInput(this);" onkeyup="checkIntInput(this, 1, 99999);event.stopPropagation();"></input>')
            
            for line in replacementHTML:
                BI.bot.browser.execute_script(f"document.getElementById('detail').insertAdjacentHTML('beforeend', '{line}');")
     
            BI.bot.browser.execute_script(f"checkIntInput(null, 1, 99999);")
        
            BI.bot.browser.execute_script(f"sendBuildRequest(null, event, false);")
                
        return True
        
    def getBuildCost(self,level=None):
        
        base_cost = self.base_build_cost
        multiplier = self.getCostMultiplier()
        
        if self.tab.code in ['shipyard','defense']:
            if level is None:
                level = 1
            return base_cost * level
        
        elif level is None:
            level = self.level+1
        else:
            level = level
            
        return base_cost * (multiplier ** (level-1))
            
    
    def __str__(self):
        #return f'({self.id}#{self.code}) {self.name}: {self.level} Lvl'   
        return f'{self.name}: {self.level} Lvl'# [UPGRADE] {self.getBuildCost()}'  
        
    
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
    
    @classmethod
    def getBuildableItems(cls):
        x = []
        for item in cls.buildables:
            if item.canBuild() and item.level != -1:
                x.append(item)
        return x
    
    
    
    
    
