# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 14:00:43 2017

@author: esppk
"""
#
#import sys
#input_ = str(sys.argv[1])

input_ = """000260701680070090190004500820100040004602900050003028009300074040050036703018000"""

#%%

    #define sudoku dictionary
letters = ["A","B","C","D","E","F","G","H","I"]
num = [x for x in range(1,10)]
def domain(input_):    
    #input_ = "232"*3*9
    sudo = dict()
    
    ii = 0
    for l in letters:
        row = [l]*9
        for ll, n in zip(row, num):
            idx = ll+str(n)
            sudo[idx] = [int(input_[ii])]
            ii+=1
    
    
    #initialized domain for each cell
    
    for cell in sudo.keys():
        if sudo[cell] == [0]:
            sudo[cell] = num.copy()  
    return sudo

#%%
#define contrains

def contrains():        
    c_group = set()
    
    #Row contrains
    for l in letters:
        for n in num:
            others = num.copy()
            others.remove(n)
            for j in others:
                c_group.add((l+str(n), l+str(j)))
    
    #Col contrains
                
    for n in num:
        for l in letters:
            others = letters.copy()
            others.remove(l)
            for j in others:
                c_group.add((l+str(n), j+str(n)))
                
    
    #for each unit
    
    split_idx = [[0,1,2],[3,4,5],[6,7,8]]
    
    for u in split_idx:
        for v in split_idx:
            sub_letters = []
            sub_num = []
            for i,j in zip(u,v):
                sub_letters.append(letters[i])
                sub_num.append(num[j])
            
            elem = []
            for l in sub_letters:
                for n in sub_num:
                    elem.append(l+str(n))
                    
            for e in elem:
                others = elem.copy()
                others.remove(e)
                for o in others:
                    c_group.add((e,o))
    
    return c_group

#Generating Neighbors
c_group = contrains()
    
neighbors = dict()
for value, key in c_group:
    if key not in neighbors.keys():
        neighbors[key] = []
    neighbors[key].append((value, key)) 

    
    
#%%

#AC-3

def AC3(sudo, arcs):
    while arcs != set(): 
 #   for count_ in range(30):    
        each  = arcs.pop()
        x_i = each[0]
        x_j = each[1]
        iter_list = sudo[x_i].copy()
        for d in iter_list:
            if (d in sudo[x_j]) and (len(sudo[x_j]) == 1):
                sudo[x_i].remove(d)
                if sudo[x_i] == []:
                    return False
                for neigh in neighbors[x_i]:
                    arcs.add(neigh)
    return True, sudo
    
                    
#%%


             
#%%
def Check_assignment(sudo):
    c = contrains()
    for each in c:
        x = each[0]
        y = each[1]
        if sudo[x] == sudo[y]:
            return False
    for each in sudo.values():
        if each == 0:
            return False
    return True



#%%

def unassigned(sudo):   
    unassinged_var = []
    for key in sudo.keys():
        if sudo[key] == 0:
            unassinged_var.append(key)
    return unassinged_var


def ordered_value(unassinged_var, sudo):
    max_ = 9
    for each in unassinged_var:
        l = len(sudo[each])
        if l < max_:
            max_ = l
            candidate = each
            
    return candidate, sudo[candidate]
        

def initial_assign(sudo):
    assign = sudo.copy()
    for key in assign.keys():
        if len(sudo[key]) == 1:
            assign[key] = sudo[key][0]
        else:
            assign[key] = 0
    return assign


#Backtracking search
def bts(assign, sudo):
    if Check_assignment(assign):
        return assign
    
    unassigned_cells = unassigned(assign)
    key,values = ordered_value(unassigned_cells, sudo)
    for v in values:
        assign[key] = v
        #check neighbors
        marker = []
        infer = True
        for each in neighbors[key]:
            x = each[0]
            
            if v in sudo[x]:
                sudo[x].remove(v)
                if len(sudo[x]) == 0:
                    infer = False
                marker.append(x)
                
        if infer != False:
            result = bts(assign, sudo)
            if result != False:
                return result
        
        assign[key] = 0
        for each in marker:
            sudo[each].append(v)
            
    return False

#%%

ii = 0
idx = []
for l in letters:
    row = [l]*9
    for ll, n in zip(row, num):
        idx.append(ll+str(n))


#with open("sudokus_start.txt") as f:
#    inputs = f.readlines()
#    
#with open("sudokus_finish.txt") as f:
#    solutions = f.readlines()

#input_ = inputs[0]    
sudo = domain(input_)
_, sudo = AC3(sudo, c_group)   
if Check_assignment(sudo):
    result = sudo
    s = ""
    for k in idx:
        v = result[k]
        s += str(v[0])
    tag = " AC3"
else:
    assign = initial_assign(sudo)
    result = bts(assign, sudo)
    tag = " BTS"
    
    s = ""
    for k in idx:
        v = result[k]
        s += str(v)       
                    


s = s + tag 
        
        
with open("output.txt", "w") as f:
    f.write(s)    
    

            
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    