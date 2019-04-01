#============ Nielsen ================
# Created: 22/03/2019 / 
# Created by Jeiso Silva
#=====================================
#--------------------------------------------------------------------------------------------------------------------------------------------- 
import pandas as pd  
def dobra(lista):
    
    pos = 0
    val = []
    while pos < len(lista):
        lista[pos] *= 2
        val = lista[pos]
        pos += 1
    return lista


def soma(*num):
    s = 0
    for i in num:
        s += i
    print(f'\033[0;31mSomando os valores {num} temos {s}.\033[m')  
        
def panda():
    df = pd.read_csv('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_massivo/_model-file/csv-modelo.csv',delimiter = ';')
    print(df)

