from utils import Utils
import math

class Resources:
    def __init__(self,metal=0,crystal=0,deuter=0,energy=0,dic=None):
        if dic:
            self.metal = int(Utils.removePunctuation(dic.get('metal',0)))
            self.crystal = int(Utils.removePunctuation(dic.get('crystal',0)))
            self.deuter = int(Utils.removePunctuation(dic.get('deuter',0)))
            self.energy = int(Utils.removePunctuation(dic.get('energy',0)))
        else:
            self.metal = int(Utils.removePunctuation(metal))
            self.crystal = int(Utils.removePunctuation(crystal))
            self.deuter = int(Utils.removePunctuation(deuter))
            self.energy = int(Utils.removePunctuation(energy))
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
        return True
        
        
    def isPositive(self):
        return not self.isNegative()
        
        
    def pay(self,other,skip_energy=True):
        self -= other
        if skip_energy and self.energy < 0:
            self.energy = 0
        return Resources(dic=self.__dict__())
        
        
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
        return f'Metal: {self.metal_f}  Kryształ: {self.crystal_f}  Deuter: {self.deuter_f}  Energia: {self.energy_f}'
    
    
