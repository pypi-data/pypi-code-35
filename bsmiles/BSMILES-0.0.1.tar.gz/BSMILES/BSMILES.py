#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 21:07:29 2018

@author: loku
"""


from rdkit import Chem
import time
cur_time = time.asctime(time.localtime(time.time()))
print("version_12_2.py"+str(cur_time))
double1 = {'L': 'Cl', 'B': 'Br', 'D': '[C@@H]', 'E': '[C@H]', 'Z': '[nH]', 'Y': '[N+]', 'X': '[O-]', 'W': '[n+]', 'V': '[N-]'}
double2 = {'Cl': 'L', 'Br': 'B', '[C@@H]': 'D', '[C@H]': 'E', '[nH]': 'Z', '[N+]': 'Y', '[O-]': 'X', '[n+]': 'W', '[N-]': 'V'}
unvisit = ["a","g","h","j","m","q","r","t","u","A","G","H","J","M","Q","R","T","U"]
ring_stru = ["useless","!","%","&","*","+",",",";","<",">"]
class fragmentNode:
    def __init__(self,x,y,z,n):
        self.atomlist = x
        self.bondlist = y
        self.notation = z
        self.nei_atom = n
        #self.visited = False

def filter_3rings(mol):
    ringInfo = mol.GetRingInfo()
    atom_in_ring = ringInfo.AtomRings()
    for ring in atom_in_ring :
        for atom in ring:
            num_rings = ringInfo.NumAtomRings(atom)
            if num_rings > 2:
                return True
    return False
    
def find_fragment(cur_idx, mol):
    stack = []
    pare = []
    stack.append(cur_idx)
    bondlist = []#visited
    atomlist = []
    nei_atom = []
    nei_bond = []
    notation = ""
    sublist = []
    count = {}
    while stack :#DFS 
        #cur_idx = stack.top()[0]忘了这个想法
        cur_idx = stack[-1]
        flag = False
        
        atom = mol.GetAtomWithIdx(cur_idx)
        ringInfo = mol.GetRingInfo()
        bonds = [bond.GetIdx() for bond in atom.GetBonds()]#bond type
        num = ringInfo.NumAtomRings(cur_idx)
        #nei_bond include all nei bonds of this fragment
        bonds = list(set(bonds) - set(bondlist) - set(nei_bond))
        #bonds = list(set(bonds) - set(bondlist))
        if cur_idx in atomlist:#判断当前点是不是访问过
            flag = True
            #n = count[cur_idx]
        else:#当前点没有被访问过
            atomlist.append(cur_idx)
            for b in bonds:
                bond = mol.GetBondWithIdx(b)
                atom2 = bond.GetOtherAtom(atom)
                idx = atom2.GetIdx()
                if idx in atomlist:
                    bondlist.append(b)
                    n = count[idx]
                    count[idx] = n - 1
                    pare.append((cur_idx,idx))
                    continue
                    #这里可以获取环破的地方
                num2 = ringInfo.NumAtomRings(idx)
                inR = bond.IsInRing()
                if inR or not inR and num2 == 0 and num == 0:
                    #判断邻边是不是和当前点在同一个结构里面
                    continue
                else:
                    nei_bond.append(b)
                    nei_atom.append(idx)
            bonds = list(set(bonds) - set(bondlist) - set(nei_bond))
            count[cur_idx] = len(bonds)#number of nei_bon of cur_atom
        a_s = atom.GetSmarts()
        
        new =[]
        if len(a_s) > 1:#对【c@】这种符号进行处理
            new.append(a_s)
            if a_s in double2.keys():
                a_s = double2[a_s]
            else:
                u = unvisit.pop()
                double2[a_s] = u
                double1[u] = a_s
        else:
            pass
        if bonds and not flag:
            for b in bonds :
                bond = mol.GetBondWithIdx(b)
                atom2 = bond.GetOtherAtom(atom)
                idx = atom2.GetIdx()
                stack.append(b)
                bondlist.append(b)
                stack.append(idx) 
                break
        elif bonds and flag:
            sublist.append("(" + notation + ")")
            notation = ""
            for b in bonds :
                bond = mol.GetBondWithIdx(b)
                atom2 = bond.GetOtherAtom(atom)
                idx = atom2.GetIdx()
                stack.append(b)
                bondlist.append(b)
                stack.append(idx)
                break
        elif not bonds and not flag:
            
            if len(stack) == 1:#come to the bot
                notation = a_s + notation
                stack.pop()
            else:
                notation = a_s
                stack.pop()
                b = stack.pop()#get bond info
                bond = mol.GetBondWithIdx(b)
                #这个bond和atom的顺序对吗？
                ring_p = ""
                #break_b_symbol = ""
                for i,p in enumerate(pare):
                    if cur_idx in p:
                        #ring_p += str(i+1)
                        break_b = mol.GetBondBetweenAtoms(p[0],p[1])
                        break_b_symbol = break_b.GetSmarts()
                        ring_p += break_b_symbol
                        ring_p += ring_stru[i+1]
                #notation =  bond.GetSmarts() + a_s + break_b_symbol + ring_p
                notation =  bond.GetSmarts() + a_s + ring_p
                #sublist.append( notation )
                #notation = ""
        else:
            s = ""
            x = count[cur_idx]
            #if x > 1:#这样做是因为不经过分岔点的没有放入sub里面
            #现在不经过的也放到sub里面
            for i  in range (x -1 ):#did not append last sub
#                sub = sublist[0]
#                s += sub
#                if len(sublist) - 1  != 0:
#                    sublist = sublist[1:]
#                else:
#                    sublist = []
                #这里要确保每次选择的子集是属于当前点的，所以从后往前加
                sub = sublist.pop()
                #但是会出现atomlist里面排前面的atom符号出现在了后面
                #因此这里是s = sub + s
                s = sub + s
            if len(stack) == 1:
                ring_p = ""
                stack.pop()
                for i,p in enumerate(pare):
                    if cur_idx in p:
                        #ring_p += str(i+1)
                        ring_p += ring_stru[i+1]
                notation = a_s + ring_p + s + notation
                #sublist.append("(" + notation)
            else:
                stack.pop()
                b = stack.pop()
                bond = mol.GetBondWithIdx(b)
                ring_p = ""
                #break_b_symbol = ""
                for i,p in enumerate(pare):
                    if cur_idx in p:
                        #ring_p += str(i+1)
                        break_b = mol.GetBondBetweenAtoms(p[0],p[1])
                        break_b_symbol = break_b.GetSmarts()
                        ring_p += break_b_symbol
                        ring_p += ring_stru[i+1]
                #notation = bond.GetSmarts() + a_s + break_b_symbol + ring_p + s + notation
                notation = bond.GetSmarts() + a_s + ring_p + s + notation
                #sublist.append("(" + notation + ")")
    fragment = fragmentNode(atomlist,bondlist,notation,nei_atom)
    return fragment

def formA_(idx,mol,visited):#nei_pare最好存一对，这样还方便确认bond
    fragment = find_fragment(idx, mol)
    s = fragment.notation
    visited += fragment.atomlist
    nei = fragment.nei_atom
    nei = list(set(nei) - set(visited))
    if nei:
        sublist = ""
        non_c_sublist  = ""
        bond_symbol = ""
        for n in nei:
            atomlist = fragment.atomlist
            atom = mol.GetAtomWithIdx(n)
            for a in atom.GetNeighbors():
                i = a.GetIdx()
                if i in atomlist:
                    bond = mol.GetBondBetweenAtoms(i,n)
                    bond_symbol = bond.GetSmarts()
                    break
            p = atomlist.index(i)
            notation, non_c_notation,visited = formA_(n,mol,visited)
            sublist = sublist + "{" + str(p) + bond_symbol + notation + "}"
            non_c_sublist =  non_c_sublist + "{" + bond_symbol + notation + "}"
        return fragment.notation + sublist, fragment.notation + non_c_sublist,visited
            
    else:
        return fragment.notation, fragment.notation, visited


def encode(smi):
    #print(smi)
    mol = Chem.MolFromSmiles(smi)
#    right = []
#    left = []
#    
#    for s in smi:
#        if s == "\\":
#            
#        elif s == "/"
#    
    #step 1: use filter remove 3_rings
    if filter_3rings(mol):
        return "false","false"
    visited = []
    formA, non_c_formA, visited = formA_(0,mol,visited)
    return formA
#print(encode_formA("CN1CCN(CC2=c3oc(=O)/c(=C4\C=CC=CN4)cc3C=CC2=O)CC1"))
    
#import pickle
#
#f = open("smiles_validAll.txt","rb")
#smiles = pickle.load(f)
#f.close()
##smiles = "O=C(CN(Cc1ccc(F)cc1)C(=O)CCC(=O)Nc1ccccn1)NCc1ccco1"
#count = 0
#i = 0
#bsmiles = []
#for s in smiles:
#    i += 1
#    #print("smiles" + str(i) + ":  ",s)
##    !!
#    formA,non_c_formA = encode_formA(s)
#    if formA == "false":
#        continue
#    else:
#        bsmiles.append(formA)
#f = open("bsmiles_valid","wb")
#pickle.dump(bsmiles,f)
#f.close()

    




