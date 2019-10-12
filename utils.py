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