import argparse
import sys
import xml.etree.ElementTree as etree

import triz2sce_func

print('triz2sce 1.0.8.post1 190323 (c) 2018 Pedro Fernández.')

parser = argparse.ArgumentParser()
parser.add_argument("in_file", help='Fichero de entrada')
parser.add_argument("out_file", help='Fichero de salida', nargs='?')
parser.add_argument('-p1', help="Mensajes de sistema en primera persona", action="store_true")
parser.add_argument('-e',help="Create an english DAAD template", action='store_true')

args=parser.parse_args()

in_file=args.in_file
out_file=args.out_file

if out_file==None:
        out_file=in_file.lower()
        if out_file.endswith('.trizbort'):
                out_file=out_file.replace('.trizbort','.sce')
        else:
                out_file=out_file+'.sce'
else:
        out_file=out_file.lower()
        if not out_file.endswith('.sce'):
                out_file=out_file+'.sce'

if args.e:
        print('English temnplate selected')
        english=True
else:
        english=False

tree=etree.parse(in_file)
root=tree.getroot()
info=root[0]
map=root[1]

# Valores por defecto para título, autor, etc...
if english:
        title='Test adventure generated with triz2sce.'
        author='Anonymous'
        description='Test adventure for the conversion script triz2sce (trizbort maps to DAAD SCE source code).'
        history='Adventure introduction text.'
else:
        title='Aventura de prueba generada con triz2sce.'
        author='Anónimo'
        description='Aventura de prueba del script conversor triz2sce (mapas de trizbort a código fuente SCE del DAAD).'
        history='Texto introductorio de la aventura.' 

# Los sustituye por los del elemento 'info' del mapa si los hubiera

for x in info:
        if x.tag=='title':
                title=x.text
        if x.tag=='author':
                author=x.text
        if x.tag=='description':
                description=x.text
        if x.tag=='history':
                history=x.text

rooms=map.findall('room')
lines=map.findall('line')

listRooms=[]
listObjects=[]
startRoom=1

if english:
        print ('Creating locations and objects list.')
else:
        print ('Creando lista de localidades y objetos.')
loc=1
for y in rooms:
        if y.get('isStartRoom')=='yes':
                startRoom=loc
        listRooms.append([y.get('description'),y.get('id'),loc])
        x=y.find('objects')
        if x!=None:
                if x.text!=None:
                        a=x.text.strip('|')
                        l=a.split('|')
                        for p in l:
                                # Añadido en 1.0.8b2. Comprobación adicional de que el nombre del objeto no es una cadena nula ni espacios en blanco.
                                p=p.strip()
                                if p!='':                                
                                        genero=0
                                        numero=0
                                        propio=0
                                        ropa=0
                                        contenedor=0
                                        if '[m]' in p:
                                                genero=1
                                                p=p.replace('[m]','')
                                        if '[f]' in p:
                                                genero=2
                                                p=p.replace('[f]','')
                                        if '[1]' in p:
                                                numero=1
                                                p=p.replace('[1]','')
                                        if '[2]' in p:
                                                numero=2
                                                p=p.replace('[2]','')
                                        if '[!]' in p:
                                                propio=1
                                                p=p.replace('[!]','')
                                        if '[w]' in p:
                                                ropa=1
                                                p=p.replace('[w]','')
                                        if '[c]' in p:
                                                contenedor=1
                                                p=p.replace('[c]','')        
                                                
                                        listObjects.append([triz2sce_func.acentos(p.split()[0]).upper(), loc, p.lower(), genero, numero, propio, ropa, contenedor])
                                else:
                                        if english:
                                                print('WARNING: ignored object with invalid name at location', loc, '-', y.get('name'))
                                        else:
                                                print('ATENCIÖN: se ha ignorado un objeto de nombre no válido en la localidad', loc, '-', y.get('name'))
        loc=loc+1

# Añadido en 1.0.8
# Separa la los objetos con el atributo 'contenedor' [c] en una lista aparte       

listContainers=[]
listContainers=[y for y in listObjects if y[7]==1]                
listObjects=[y for y in listObjects if y[7]==0]

# Si no hay objetos (normales), crea una linterna como objeto dummy (como en la plantilla original)

if listObjects==[]:
        if english:
                listObjects.append(['TORCH',0,'a torch (lit)',0,0,0,0,0])
        else:
                listObjects.append(['LINTERNA',0,'una linterna (encendida)',0,0,0,0,0])

for y in listContainers:
        listObjects.insert(1,y)

if listContainers != []:
        if english:
                cadena='; Fake location meant to support some container object.'
        else:
                cadena='; Localidad falsa para dar soporte a un objeto contenedor.'
        for y in listContainers:
                listRooms.insert(0,[cadena,'',0])
        cont=1        
        for y in listRooms:
                y[2]=cont
                cont=cont+1
        startRoom=startRoom+len(listContainers)
        for y in listObjects:
                y[1]=y[1]+len(listContainers)


if english:
        print('Creating connections list.')     
else:   
        print('Creando lista de conexiones.')   
for y in listRooms:
        a=[]
        for x in lines:
                w=x.findall('dock')
                if len(w)==2:
                        for z in w:
                                if y[1]==z.get('id'):
                                        if z.get('index')=='0':
                                                b=triz2sce_func.dirTransform2(x.get('startText'), english)
                                                if b!=None:
                                                        a.append(b+' '+triz2sce_func.id2loc(w[1].get('id'),listRooms))
                                                else:   
                                                        a.append(triz2sce_func.dirTransform(z.get('port'), english)+' '+triz2sce_func.id2loc(w[1].get('id'),listRooms))
                                        else:
                                                if x.get('flow')!='oneWay':
                                                        b=triz2sce_func.dirTransform2(x.get('endText'), english)
                                                        if b!=None:
                                                                a.append(b+' '+triz2sce_func.id2loc(w[0].get('id'),listRooms))
                                                        else:
                                                                a.append(triz2sce_func.dirTransform(z.get('port'), english)+' '+triz2sce_func.id2loc(w[0].get('id'),listRooms))                         
        y.append(a)     


# Abre fichero
        
f=open(out_file,'w',encoding='850', newline='\r\n')

triz2sce_func.imprimeDEF(f, english)    # Imprime sección /DEF
triz2sce_func.imprimeCTL(f, english)    # Imprime sección /CTL
if english:
        triz2sce_func.imprimeTOK_ENG(f) # Print english /TOK section
else:
        triz2sce_func.imprimeTOK(f)     # Imprime sección /TOK
if english:
        triz2sce_func.imprimeVOC_ENG(f)
else:
        triz2sce_func.imprimeVOC(f)     # Imprime sección /VOC (primera parte)

# Inserta objetos del usuario en sección /VOC

x=50
print('; Objetos definidos por el usuario en el mapa visual, si los hubiera', file=f)
for y in listObjects:
        print (y[0]+'      '+str(x)+'      noun',file=f)
        x=x+1

if english:
        triz2sce_func.imprimeVOC2_ENG(f)                # Prints english /VOC section (second part)
else:
        triz2sce_func.imprimeVOC2(f)                    # Imprime sección /VOC (saegunda parte)

if args.p1:
        if english:
                triz2sce_func.imprimeSTX1p_ENG(f)       # Prints english 1st person /STX section
        else:
                triz2sce_func.imprimeSTX1p(f)           # Imprime sección /STX en primera persona
else:
        if english:
                triz2sce_func.imprimeSTX2p_ENG(f)       # Prints english 2nd person /STX section
        else:
                triz2sce_func.imprimeSTX(f)             # Imprime sección /STX en segunda persona
if english:
        triz2sce_func.imprimeMTX_ENG(f, history)                        # Prints english /MTX section
else:
        triz2sce_func.imprimeMTX(f, history)                    # Imprime sección /MTX


                        
x=1
z=1+len(listContainers)
for y in rooms:
        print('/'+str(15+x), file=f)
        if y.get('subtitle')!='':
                print(y.get('subtitle')[:26], file=f)
        else:
                if y.get('name')!='Cave':
                        print(y.get('name')[:26], file=f)
                else:
                        if english:
                                print('Location '+str(z), file=f)
                        else:
                                print('Localidad '+str(z), file=f)
        x=x+1
        z=z+1
        
helpMessage1=x + 15
helpMessage2=helpMessage1 + 1

if english:
        print('/'+str(helpMessage1), file=f)
        print(' HELP SCREEN', file=f)
        print('/'+str(helpMessage2), file=f)
        print('Text adventures are text games based on exploring locations and manipulating objects next to the player character.', file=f)
        print('', file=f)
        print('', file=f)
        print('Actions are told to the computer using simple "action-object" like sentences.', file=f)
        print('', file=f)
        print('', file=f)
        print('Movements are done using cardinal points "GO NORTH", "SOUTH", "WEST" or their abreviations: N, S, E, W. Occasionally commands as "UP" or "IN" will also work.', file=f)
        print('', file=f)
        print('', file=f)
        print('Common actions with objects are "GET object", "DROP", "EXAMINE" (or its abrevation "EX"). "INVENTORY" (or "I") lists carried items. "LOOK" (or "L") redescribes the location.', file=f)
        print('', file=f)
        print(';', file=f)
        print('OK.')
else:
        print('/'+str(helpMessage1), file=f)
        print(' PANTALLA DE AYUDA', file=f)
        print('/'+str(helpMessage2), file=f)
        print('Las aventuras conversacionales son juegos de texto basados en la exploración de localidades y la manipulación de objetos al alcance inmediato del protagonista.', file=f)
        print('', file=f)
        print('', file=f)
        print('Las acciones se comunican al ordenador mediante frases sencillas del tipo "acción-objeto".', file=f)
        print('', file=f)
        print('', file=f)
        print('El movimiento se efectua mediante puntos cardinales "IR NORTE", "SUR", "OESTE" o sus abreviaturas: N, S, E, O. Ocasionalmente órdenes como "SUBIR", o "ENTRAR" también funcionarán.', file=f)
        print('', file=f)
        print('', file=f)
        print('Acciones comunes con los objetos son "COGER objeto", "DEJAR", "EXAMINAR" (o su abreviatura "EX". "INVENTARIO" (o "I") lista los objetos llevados. "MIRAR" o "M" redescribe la localidad.', file=f)
        print('', file=f)
        print(';', file=f)
        print('OK.')


# Imprime sección /OTX

if english:
        print('Printing english /OTX section',end=' -> ')
        print('/OTX',file=f)
        x=0
        for y in listObjects:
                print('/'+str(x),file=f)
                a=''
                if y[4]!=2:
                        a='a '
                else:
                        a='some '
                print(a+y[2],file=f)
                x=x+1
        print(';', file=f)
        print('OK.')    
else:
        print('Imprimiendo sección /OTX',end=' -> ')
        print('/OTX',file=f)
        x=0
        for y in listObjects:
                print('/'+str(x),file=f)
                a=''
                if y[3]==1:
                        a='un '
                        if y[4]==2:
                                a='unos '
                if y[3]==2:
                        a='una '
                        if y[4]==2:
                                a='unas '
                print(a+y[2],file=f)
                x=x+1
        print(';', file=f)
        print('OK.')

# Imprime sección /LTX  
if english:
        print('Printing /LTX section', end=' ->- ')
else:
        print('Imprimiendo sección /LTX',end=' -> ')    
print('/LTX',file=f)
print('/0',file=f)
print(title.title(), file=f)
print('', file=f)
print('', file=f)
if english:
        print('by: ',triz2sce_func.acentos(author).upper(), file=f)
else:
        print('por: ',triz2sce_func.acentos(author).upper(), file=f)
print('', file=f)
print('', file=f)
print(description, file=f)
print('', file=f)
print('', file=f)
x=1
for y in listRooms:
        print('/'+str(x),file=f)
        if (y[0]!=''):
                print(y[0],file=f)
        else:
                if english:
                        print('Location '+str(x)+' description', file=f)
                else:
                        print('Descripción localidad '+str(x), file=f)
        x=x+1
print(';', file=f)
print('OK.')    
        
# Imprime sección /CON
if english:
        print('Printing /CON section',end=' -> ')
else:
        print('Imprimiendo sección /CON',end=' -> ')
print('/CON',file=f)
print('/0',file=f)
x=1
for y in listRooms:
        print('/'+str(x),file=f)
        if y[3]!=[]:
                for z in y[3]:
                        print(z,file=f)
        x=x+1
print(';', file=f)
print('OK.')

# Imprime sección /OBJ
if english:
        print('Printing /OBJ section',end=' -> ')
else:
        print('Imprimiendo sección /OBJ',end=' -> ')
print ('/OBJ',file=f)
print(';obj  starts  weight    c w  5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0    noun   adjective', file=f)
print(';num    at', file=f)
x=0
for y in listObjects:
        cadena=''
        cadena = cadena + '/' + str(x) + ' ' + str(y[1]) + ' ' + '1' + ' '
        if y[7]==0:
                cadena=cadena + '_ '
        else:
                cadena=cadena+'Y '
        if y[6]==0:
                cadena=cadena+'_   '  
        else:
                cadena=cadena+'Y   '
        cadena=cadena+'_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  '+y[0]+' _'
        print(cadena, file=f)
        x=x+1
print(';', file=f)
print('OK.')

triz2sce_func.imprimePRO0(f, english)                                                   # Imprime sección /PRO 0
triz2sce_func.imprimePRO1(f, english)                                                   # Imprime sección /PRO 1
triz2sce_func.imprimePRO2(f, english)                                                   # Imprime sección /PRO 2
triz2sce_func.imprimePRO3(f, english)                                                   # Imprime sección /PRO 3
triz2sce_func.imprimePRO4(f, english)                                                   # Imprime sección /PRO 4
if english:
        triz2sce_func.imprimePRO5_ENG(f, helpMessage1, helpMessage2, listContainers)    # Prints english /PRO 5 section
else:
        triz2sce_func.imprimePRO5(f, helpMessage1, helpMessage2, listContainers)                        # Imprime sección /PRO 5
triz2sce_func.imprimePRO6(f,startRoom, english)                                         # Imprime sección /PRO 6
triz2sce_func.imprimeOtrosPros(f, english)                                              # Imprime otros PROs

# Imprime la parte de PRO 11 que pone el atributo subtitle en la barra de estado

# Si hay contenedores, elimina de la lista de localidades las localidades falsas
# creadas para darles soporte

      
if listContainers!=[]:
        listRooms=listRooms[len(listContainers):]


x=1+len(listContainers)
z=1
for y in listRooms:
        print('_       _       AT '+str(x), file=f)
        print('                MES '+str(z+15), file=f)
        print('', file=f)
        x=x+1
        z=z+1

triz2sce_func.imprimeOtrosPros2(f, english)             # Imprime otros PROs

# Cierra fichero

f.close()

        





