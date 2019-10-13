class Utils:
    @staticmethod
    def thousandSeparate(value,separator='.'):
        v = str(value)
        if len(v) == 4:
            return v
        
        rv = list(reversed(v))
        for i,char in enumerate(rv):
            if not i%3 and i > 0:
                rv[i] = char+separator
        v = ''.join(list(reversed(rv)))
        return v
    
    @staticmethod
    def removePunctuation(value):
        if not isinstance(value,str):
            return value
        value = value.replace('.','').replace(' ','').replace(',','')
        return value