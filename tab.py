from bot_instance import BI
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Tab:
    all_tabs = {}
    base_url = 'https://s163-pl.ogame.gameforge.com/game/index.php?page='
    
    def __init__(self,code):
        Tab.all_tabs[code] = self
        self.code = code
        self.url = Tab.base_url + code
        self.token = None
        
    def open(self):
        if BI.bot.getCurrentTab() == self:
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