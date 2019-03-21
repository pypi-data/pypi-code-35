#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 16:27:14 2019

@author: xiaochun

"""

"""
convert bsmiles back to smiles
call function "convertB"
"""
ring_stru = ["useless","!","%","&","*","+",",",";","<",">"]
#ring_stru = ["useless","!","$","%","&","*","+",",","-","."]
def combin(parent,child,dic):
    atom_mark = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    atom_mark2 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    mark = atom_mark + atom_mark2
    position = ""
    for s in child:
        if not s.isdigit():
            break
        position += s
    l = len(position)
    position = int(position)
    count = -1
    for i,s in enumerate(parent):
        if s.isdigit() or s not in mark :
            continue
        else:
            count += 1
            if count == position:
                break
    idx = len(dic)
    key = "!" + str(idx) + "!"
    dic[key] = child[l:]
    parent = parent[:i + 1] + "(" + key + ")" +parent[i + 1:]
    return parent,dic            
    
def insert_sub(smi,dic):
    flag = False
    smi2 = ""
    idx = ""
    start = False
    for s in smi:
        if s == "!" and len(idx) == 0:
            start = True
            continue
        elif s == "!" and len(idx)!= 0:
            start = False
            idx = int(idx)
            idx = "!" + str(idx) + "!"
            smi2 += dic[idx]
            idx = ""
            flag = True
            continue
        if start == False:
            smi2 += s
            continue
        idx += s
    return smi2,flag

def change_no(content,ring_p):
    smi = ""
    visited = {}
    position = ""
    for s in content:
        if not s.isdigit():
            break
        position += s
    l = len(position)
    content = content[l:]
    for s in content:
        if s.isdigit() and int(s) not in visited.keys():
            visited[int(s)] = str(ring_p)
            smi += str(ring_p)
            ring_p += 1
            continue
        elif s.isdigit() and int(s) in visited.keys():
            
            smi += visited[int(s)]
            continue
        smi += s
    return position + smi,ring_p

def convertB(bsmiles):
    #bsmiles:string
    double1 = {'L': 'Cl', 'B': 'Br', 'D': '[C@@H]', 'E': '[C@H]', 'Z': '[nH]', 'Y': '[N+]', 'X': '[O-]', 'W': '[n+]', 'V': '[N-]'}
#    double2 = {'Cl': 'L', 'Br': 'B', '[C@@H]': 'D', '[C@H]': 'E', '[nH]': 'Z', '[N+]': 'Y', '[O-]': 'X', '[n+]': 'W', '[N-]': 'V'}
#    unvisit = ["a","g","h","j","m","q","r","t","u","A","G","H","J","M","Q","R","T","U"]
    
    double = ['L', 'B', 'D', 'E', 'Z', 'Y', 'X', 'W', 'V']
    lev_no = 0
    level_list = [[0]]
    content = ""
    dic = {}
    smi = ""
    for s in bsmiles:
        if s in ring_stru:
            i = ring_stru.index(s)
            smi += str(i)
            continue
        
        smi += s
    ring_p = 1
    for s in smi:
        if s == "{":
            if len(content) != 0 and len(level_list) > lev_no:
                content,ring_p = change_no(content,ring_p)
                level_list[lev_no].append(content)
            elif len(content) != 0:
                content,ring_p = change_no(content,ring_p)
                level_list.append([content])
            lev_no += 1
            content = ""
            continue
        elif s == "}":
            if len(content) != 0:
                content,ring_p = change_no(content,ring_p)
                parent = level_list[lev_no - 1].pop()
                parent,dic = combin(parent,content,dic)
                level_list[lev_no - 1].append(parent)
            else:
                parent = level_list[lev_no - 1].pop()
                child = level_list[lev_no].pop()
                parent,dic = combin(parent,child,dic)
                level_list[lev_no - 1 ].append(parent)
            lev_no = lev_no - 1
            content = ""
            continue
        content += s
    if len(content) != 0:#it means no {} in this string
        level_list[0].append(content)
        
    smi = level_list[0]
    smi = smi[1]
    
    #location = []
    flag = True
    while flag:
        smi,flag = insert_sub(smi,dic)
    
    #add ring number and [c@@h] cl br 
    smi2 = ""
    for s in smi:
        if s in double:
            i = double1[s]
            smi2 += i
            continue
        smi2 += s
    
    return smi2        

"""
seperate bsmiels into fragments
"""
import pickle
from rdkit import Chem

def getFragments(visited,bsmiles):
    #visited:list
    #bsmiles:string
    content =""
    fragments= []
    for s in bsmiles:
        if s == "{":
            position = ""
            if len(content) != 0:
                for c in content:
                    if c.isdigit():
                        position += c
                    else:
                        break
                l = len(position)
                fragments.append(position)
                if content[l:] not in visited:
                    visited.append(content[l:])
                fragments.append(content[l:]) 
                
                content = ""
            
            fragments.append("{")
                
            continue
        elif s == "}":
            position = ""
            if len(content) != 0:
                for c in content:
                    if c.isdigit():
                        position += c
                    else:
                        break
                l = len(position)
                fragments.append(position)
                if content[l:] not in visited:
                    visited.append(content[l:])
                fragments.append(content[l:]) 
                content = ""
            fragments.append("}")
                
            continue
        content += s
    if len(content ) != 0:
        if content not in visited:
            visited.append(content)
        fragments.append(content)
    return visited,fragments



def bsmiles_to_frag(inputfile,outputfile):
    #inputfile:filenam(string)
    #outputfile:filename(string)
    f = open(inputfile,"rb")
    bsmiles = pickle.load(f)
    f.close()
    fragments = []
    i = 0
    visited = []
    for s in bsmiles:
        #print("bsmiles:          ",s)
        i += 1
        #s = "CC(=O)N{3c!scnc!{4-c!cccs!}{2NC=O{1c!ccccc!}}}"
        visited,frag = getFragments(visited,s)#visited 是用来测试一共有多少个fragment
        fragments.append(frag)

    f = open(outputfile,"wb")
    pickle.dump(fragments,f)
    f.close()
    
"""
make sure that every bsmiles seperated into correct fragments.
"""
def result_test(fragments,bsmiles):
    #fragments: [fragment:string,fragment:string,...]
    #bsmiles:string
    ss = ""
    for j in fragments:
        ss += j
    if ss != bsmiles:
        return False
    try:
        smiles = convertB(ss)
        #print("smiles1:           ",smiles)
        mol = Chem.MolFromSmiles(smiles)
        smile2 = Chem.MolToSmiles(mol)
    except:
        return False
    return True
    