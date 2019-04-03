
from ethics.language import *

def makeSetOfAlternatives(*models):
    for m in models:
        m.setAlternatives(*models)
        
def makeSetOfEpistemicAlternatives(*models):
    for m in models:
        m.setEpistemicAlternatives(*models)
        m.probability = 1/len(models)
        

def mapBackToFormulae(l, m): # l: model, m: map
    erg = []
    for ll in l:
        found = False
        for mm in m:
            if m[mm] == ll:
                erg.append(eval(mm))
                found = True
                break
        if(found == False):
            for mm in m:
                if m[mm] + ll == 0:
                    erg.append(Not(eval(mm)))
                    break
    return erg
