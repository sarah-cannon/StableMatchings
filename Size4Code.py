# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:29:07 2021

@author: scannon
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from itertools import permutations
import pickle

# Set number of people on each side
n = 4

#set range restrictions
k1 = 3
k2 = 3

#Make list of preference lists 
AllAPrefLists = []
AllBPrefLists = []

#A function that takes in a matching, preference lists for the a side, preference lists for the b side, and determines whether the matching is stable
def isStable(matching, ap, bp):
    # for all unmatched pairs
    for i in range(n):
        #iprefs = ap[i]
        #Find perople i prefers to its current match
        unstable = [j for j in range(n) if ap[i].index(j) < ap[i].index(matching[i]) and bp[j].index(i) < bp[j].index(matching.index(j))]
        if len(unstable) > 0:
            return False                                                                                
            #for j in iprefers:
            #check if j perfers i to its current match
            #jprefs = bp[j]
            #if jprefs.index(i) < jprefs.index(matching.index(j)):
                #return False
    return True 

# Find all possible preference lists
for j1 in list(permutations(range(n))):
    for j2 in list(permutations(range(n))):
        for j3 in list(permutations(range(n))):
            #A sinle preference list for one side is a list of four permutations of {0,1,2,3}, 
            # The first tuple(permutation) is the preferences for person 0, always (0,1,2,3) to reduce symmetries
            # (e.g., whoever a_0 prefers first we call b_0, whoever a_0's second choice is we name b_1, etc.)
            # The second tuple(permutation) is the preferences of person 1, etc. 
            Aprefs = [(0,1,2,3), j1, j2, j3] 
            AllAPrefLists.append(Aprefs)
            # Person b_0 may have person a_0 in any position in theire preference list
            # Assume, to reduce symetries, the other three people are in order 1,2,3
            # don't consider case where b_0's first choice is a_0: then b_0 will be paired with a_0 in every stable matching, 
            # and thus this is actulaly just a size 3 problem and not interesting here
            Bprefs1 = [(1,0,2,3), j1, j2, j3] 
            Bprefs2 = [(1,2,0,3), j1, j2, j3] 
            Bprefs3 = [(1,2,3,0), j1, j2, j3] 
            AllBPrefLists.append(Bprefs1)
            AllBPrefLists.append(Bprefs2)
            AllBPrefLists.append(Bprefs3)
            
            #Print statements to chekc this is working right
            #print(Aprefs)
            
# check have found the right number of them
# Should be (4!)^3 = 13824 things in APrefs
print(len(AllAPrefLists))

# Should be 3 * (4!)^3 = 41472 things in Bprefs
print(len(AllBPrefLists))

#Filter A-side to only have preference lists of range k1
# (Above, k1 is set to 3)
AllAPrefListsRangeFiltered = []
#Remove anything with range greater than k1 in A pref lists
# If we wanted to eliminate examples that reduce to simpler cases, could also remove
# reference lists with ranges less than 3
for prefs in AllAPrefLists:
    minpos = [n-1,n-1,n-1,n-1]
    maxpos = [0,0,0,0]
    for i in range(n):
        for j in range(n):
            val = prefs[i][j]
            if minpos[val] > j:
                minpos[val] = j
            if maxpos[val] < j:
                maxpos[val] = j
    add = True           
    for i in range(n):
        if maxpos[i]-minpos[i] > k1 - 1:
            add = False
    if add == True:
        AllAPrefListsRangeFiltered.append(prefs)
 
#Count the number of A-side preference lists with range k1
print(len(AllAPrefListsRangeFiltered)) 

#Filter B-side to only have preference lists of range k2
# (Above, k2 is set to 3)
AllBPrefListsRangeFiltered = []
#Remove anything with range 4 in B pref lists
for prefs in AllBPrefLists:
    minpos = [n-1,n-1,n-1,n-1]
    maxpos = [0,0,0,0]
    for i in range(n):
        for j in range(n):
            val = prefs[i][j]
            if minpos[val] > j:
                minpos[val] = j
            if maxpos[val] < j:
                maxpos[val] = j
    add = True           
    for i in range(n):
        if maxpos[i]-minpos[i] > k2 - 1:
            add = False
    if add == True:
        AllBPrefListsRangeFiltered.append(prefs)
        
#Count the number of A-side preference lists with range k2
print(len(AllBPrefListsRangeFiltered)) 

#NumMatchings[i] is the number of preference lists that have i stable matchings
NumMatchings = [0,0,0,0,0,0,0,0,0,0,0,0]

#Find the preference lists with 5 or 7 stable matchings
list5 = []
list7 = []

counter = 0
# Keeping track of this loop
print("There should be 1208 loops that happen now:")
for Aprefs in AllAPrefListsRangeFiltered:
    print(counter)
    counter = counter + 1
    for Bprefs in AllBPrefListsRangeFiltered:
        num = 0
        #A matching is just a permutation of {0,1,2,3} saying who the A people are paired with
        # Permutation (2,1,3,0) means a_0 is paired with b_2, a_1 is paired with b_1, 
        # a_2 is paired with b_3, and a_3 is paired with b_0
        # Find all stable matchings with these preference lists
        for match in permutations(range(n)):
            if isStable(match, Aprefs, Bprefs):
                num = num + 1
                #%print(num)       
        NumMatchings[num] = NumMatchings[num] + 1
        #The ones with 5 and 7 stable matchings are most interesting for now
        if num == 5:
            list5.append([Aprefs, Bprefs])
        if num == 7:
            list7.append([Aprefs, Bprefs])
        #print(NumMatchings)

print("Number of preference lists with various numbers of stable matchings: ")
print(NumMatchings)
# For k1 =3 and k2= 3, this is [0, 3608976, 731480, 32982, 4304, 48, 0, 2, 0, 0, 0, 0]
# I shared details of the two preference lists with 7 matchings each in the Zulip channel

# with range 4 restrictions on the B side (that is, no range restrictions), this becomes: 
#[0, 37429664, 11430560, 1112320, 118112, 7360, 128, 32, 0, 0, 0, 0]

#Find the matchings for specific preference lists
#for pair in list5:
#    print(pair)
#    for match in permutations(range(n)):
#        if isStable(match, pair[0], pair[1]):
#            print(match)

#Find 7list matchings
#for pair in list7:
#    print(pair)
 #   for match in permutations(range(n)):
 #       if isStable(match, pair[0], pair[1]):
#            print(match)