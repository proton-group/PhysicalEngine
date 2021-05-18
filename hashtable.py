class htabel:
    def __init__(self):
        self.r = 1088
        self.c = 512
        self.rounds = 24

    def xor(self, a, b):
        for i in range(len(bin(a))):
            bin(a)[i] = (bin(a)[i] or bin(b)[i]) and not (bin(a)[i] and bin(b)[i])
        return a
    
    def transposition(self):
        pass
    
    def pad(self, string):
        a = 0b0
        for sym in string:
            if type(sym) == str: 
                a += ord(sym)
                a = a << len(bin(ord(sym)))
            else:
                a = a << len(bin(sym))
                a += sym
        a << 1
        a += 0b1
        while(len(bin(a)) % self.r != 0):
            a = a << 1
        a += 0b1
        p = []
        divider = 0
        while divider + self.r <= len(bin(a)):
            print(bin(a))
            p.append(bin(a)[divider : divider + self.r-1])
            divider += self.r
        return p

    def keccak(self, data):
        pass

if __name__ == "__main__":
    tabel = htabel()