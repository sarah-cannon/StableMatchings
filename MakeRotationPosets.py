# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 16:31:49 2021

@author: scannon
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from itertools import permutations
import pickle
from networkx.algorithms import isomorphism


# Set number of people on each side
n = 4

#set range restrictions
k1 = 3
k2 = 3

#A function that takes in a matching, preference lists for the a side, preference lists for the b side, and determines whether the matching is stable
#Doing this faster than just check all possible pairs to see if they are unstable would be a way to make the code faster
def isStable(matching, ap, bp):
    # for all unmatched pairs
    for i in range(n):
        # check all j in B to see if are part of an unstable pair with i in A
        unstable = [j for j in range(n) if ap[i].index(j) < ap[i].index(matching[i]) and bp[j].index(i) < bp[j].index(matching.index(j))]
        if len(unstable) > 0:
            return False                                                                                
    #If have found no unstable pairs
    return True 

def findSuitorofB(b, match, Apref, Bpref):
    # find pair of b
    a1 = match.index(b)
    
    #find where that pair appears in B's preference listt
    startindex = Bpref[b].index(a1)
    
    #look through rest of B's preference list
    for i in range(startindex+1,n): 
        a2 = Bpref[b][i]
        #check if a2 prefers b to their currnt match 
        if Apref[a2].index(b) < Apref[a2].index(match[a2]):
            return a2
    #if no suitor
    return -1


# Code that takes in a preference list and outputs its rotation poset
def FindRotations(Apref, Bpref):
    matchlist = []
    #First find the list of all possible matchings
    for match in permutations(range(n)):
        if isStable(match, Apref, Bpref):
            matchlist.append(match)
    
    #Make a graph with these stable matchings as their vertices            
    poset = nx.DiGraph()
    poset.add_nodes_from(matchlist)
        
    #For each matching, find all A-improving rotations
    #Add to poset as edges, with label giving size of rotation
    for match in matchlist:
        #print(match)
           
        #Find suitor of each person in B
        suitors = []
        for i in range(n):
            suitors.append(findSuitorofB(i, match, Apref, Bpref))
        #print(suitors)
        
        #See if there is a rotation beginning at person a_i
        for i in range(n):
            #print("i: ", i)
            visited = [False, False,False,False]
            #Only search for rotation between i and the end of the vertices, to avoid finding same rotation twice 
            for j in range(i+1):
                visited[j] = True
            current = i
            end = False
            found = False
            rot = [i]
            while end == False:
                new = suitors[match[current]]
                #If no valid suitor, can't find a rotation
                if new == current: 
                    end = True
                elif new == -1:
                    end = True
                # If have returned to i, have found a rotation
                elif new == i:
                    found = True
                    end = True
                # If have revisited somewhere that is not i, have not found a rotation
                elif visited[new] == True:
                    end = True
                #Else keep going
                else: 
                    current = new
                    visited[current]= True
                    rot.append(current)
            if found == True:
                #print("Found rotation: ", rot)
                #Add edge to poset
                #First, find destination of this rotation
                newmatch = list(match)
                for i in rot:
                    newmatch[suitors[match[i]]] = match[i]
                poset.add_weighted_edges_from([(match, tuple(newmatch), len(rot))])
    return poset

#new comparison function so graph isomorphism function consideres edge weight
def comparison(D1,D2):
    return D1['weight'] == D2['weight']

#Takes the list of preference lists in the given file, and finds all possible state spaces 
# (up to graph isomorphism, which takes edge weights into account)
# By posets here, I mean the poset whose vertices are the matchings and 
# whose edges are the A-improving rotations, not the rotation poset
def showPosets(string):
    file= open(string, 'rb')
    list = pickle.load(file)
    file.close()
    isomlist = []
    for l in list: 
        g = FindRotations(l[0], l[1])
        found = False
        for g1 in isomlist:
            if nx.is_isomorphic(g, g1, edge_match = comparison):
                found = True;
        if found == False: 
            isomlist.append(g)
    print("All possible state spaces for this list: ")
    for g in isomlist: 
        labels = nx.get_edge_attributes(g,'weight')
        pos=nx.spring_layout(g) 
        plt.figure()
        nx.draw(g, pos)  
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)                
        plt.show()

#Find state spaces
print("7 matchings, (3,3) range restrictions: ")
showPosets('7list')
"""print("6 matchings, (3,3) range restrictions: ")
showPosets('6list')"""
print("5 matchings, (3,3) range restrictions: ")
showPosets('5list')
print("4 matchings, (3,3) range restrictions: ")
showPosets('4list')
print("3 matchings, (3,3) range restrictions: ")
showPosets('3list')

# To find the same posets for the (3,4) range restrictions, just add _asym34 to the end of the file names
# (The asymmestric case takes about 20-30 minutes to run, compared to the minute or so for the (3,3) range restrictions)
