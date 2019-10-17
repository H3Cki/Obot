from tab import Tab
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

bot = None
def initialize(cls,_bot):
    global bot
    bot = _bot
    
class GalaxyTab(Tab):
    tab_codes = ['galaxy']

    def __init__(self,code):
        self.code = code
        self.url = Tab.base_url + code


class Galaxy:
    pass

class Planet:
    pass

class Debris:
    pass