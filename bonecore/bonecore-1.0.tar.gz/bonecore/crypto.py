
import time
import hashlib
import random

class bonecore_crypto():
    def generate(self, wordarray):
        self.wordarray = tuple(wordarray)
        if len(self.wordarray) < 16:
            return 0
        self.key = str()
        for self.word in self.wordarray:
            self.entropy = str(int(time.time() * random.randint(100000000,999999999) + random.randint(100000000,999999999)))[:4]
            self.srandnum = random.randint(5,120)  # Start random number
            self.erandnum = int(self.srandnum + 4) # End random number
            self.wordhash =  hashlib.sha512(self.word.encode('utf-8')).hexdigest()[self.srandnum:self.erandnum]
            self.key += str(self.wordhash+self.entropy)
        return self.key
