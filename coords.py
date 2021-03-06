from math import floor

class Coords:
    def __init__(self,galaxy,system,position):
        self.galaxy = galaxy
        self.system = system
        self.position = position
        
    def getDistanceTo(self,destination):
        galaxy_d = 20000 * abs(self.galaxy - destination.galaxy)
        if galaxy_d: return galaxy_d
    
        system_abs = abs(self.system - destination.system)
        system_d = 2700 + (95 * system_abs) if system_abs != 0 else 0
        if system_d: return system_d
        
        position_abs = abs(self.position - destination.position)
        position_d = 1000 + (5 * position_abs) if position_abs != 0 else 0
        if position_d: return position_d
        
    def __str__(self):
        return f'{self.galaxy}:{self.system}:{self.position}'


