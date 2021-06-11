# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:29:07 2021

@author: scannon

Code for makeing all possible preference lists, and arranging them according to haw may stable matchings there are
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
k2 = 3 #change to 4 for asymmetric case

#Make list of preference lists 
AllAPrefLists = []
AllBPrefLists = []

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

# Find all possible preference lists
for j1 in list(permutations(range(n))):
    for j2 in list(permutations(range(n))):
        for j3 in list(permutations(range(n))):
            #A sinle preference list for one side is a list of four permutations of {0,1,2,3}, 
            # The first tuple(permutation) is the preferences for person 0, always (0,1,2,3) to reduce symmetries
            # (e.g., whoever a_0 prefers first we call b_0, whoever a_0's second choice is we name b_1, etc.)
            # The second tuple (permutation) is the preferences of person 1, etc. 
            Aprefs = [(0,1,2,3), j1, j2, j3] 
            AllAPrefLists.append(Aprefs)
            # Person b_0 may have person a_0 in any position in their preference list
            # Assume, to reduce symetries, the other three people are in order 1,2,3
            # don't consider case where b_0's first choice is a_0: then b_0 will be paired with a_0 in every stable matching, 
            # and thus this is actulaly just a size 3 problem and not interesting here
            Bprefs1 = [(1,0,2,3), j1, j2, j3] 
            Bprefs2 = [(1,2,0,3), j1, j2, j3] 
            Bprefs3 = [(1,2,3,0), j1, j2, j3] 
            AllBPrefLists.append(Bprefs1)
            AllBPrefLists.append(Bprefs2)
            AllBPrefLists.append(Bprefs3)
            
# check have found the right number of them
# Should be (4!)^3 = 13824 things in APrefs
print("Number of posisble A preference lists: ", len(AllAPrefLists))

# Should be 3 * (4!)^3 = 41472 things in Bprefs
print("Number of posisble B preference lists: ",len(AllBPrefLists))

#Filter A-side to only have preference lists of range k1
# (Above, k1 is set to 3)
AllAPrefListsRangeFiltered = []
#Remove anything with range greater than k1 in A pref lists
# If we wanted to eliminate examples that reduce to simpler cases, could also remove them here (but don't at the moment)
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
    #check range of i         
    for i in range(n):
        if maxpos[i]-minpos[i] > k1 - 1:
            add = False
    #If never exceed range 3
    if add == True:
        AllAPrefListsRangeFiltered.append(prefs)
 
#Count the number of A-side preference lists with range k1
print("Number of posisble A preference lists after range filtering: ", len(AllAPrefListsRangeFiltered)) 

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
print("Number of posisble A preference lists after range filtering: ", len(AllBPrefListsRangeFiltered)) 

#NumMatchings[i] is the number of preference lists that have i stable matchings
NumMatchings = [0,0,0,0,0,0,0,0,0,0,0,0]

#Find the preference lists that have various numbers of stable matchings
ListSortedByNum = [ [], [], [], [], [], [], [], []]
counter = 0
# Keeping track of this loop
print("There should be ", len(AllAPrefListsRangeFiltered), " loops that happen now:")
for Aprefs in AllAPrefListsRangeFiltered:
    #Counter to keep track of how long code is taking
    print(counter)
    counter = counter + 1
    for Bprefs in AllBPrefListsRangeFiltered:
        num = 0 #number of stable matchings for htis preference list
        #A matching is just a permutation of {0,1,2,3} saying who the A people are paired with
        # Permutation (2,1,3,0) means a_0 is paired with b_2, a_1 is paired with b_1, 
        # a_2 is paired with b_3, and a_3 is paired with b_0
        # Find all stable matchings with these preference lists
        for match in permutations(range(n)):
            if isStable(match, Aprefs, Bprefs):
                num = num + 1
                #%print(num)
        # Add in appropriate places
        ListSortedByNum[num].append([Aprefs, Bprefs])
        NumMatchings[num] = NumMatchings[num] + 1

print("Number of preference lists with various numbers of stable matchings: ")
print(NumMatchings)
# For k1 =3 and k2= 3, this is [0, 3608976, 731480, 32982, 4304, 48, 0, 2, 0, 0, 0, 0]
# I shared details of the two preference lists with 7 matchings each in the Zulip channel

# with range 4 restrictions on the B side (that is, no range restrictions), this becomes: 
#[0, 37429664, 11430560, 1112320, 118112, 7360, 128, 32, 0, 0, 0, 0]

#Pickle the preference lists for later use
file2 = open('2list', 'wb')
pickle.dump(ListSortedByNum[2], file2)
file2.close()
file3 = open('3list', 'wb')
pickle.dump(ListSortedByNum[3], file3)
file3.close()
file4 = open('4list', 'wb')
pickle.dump(ListSortedByNum[4], file4)
file4.close()
file5 = open('5list', 'wb')
pickle.dump(ListSortedByNum[5], file5)
file5.close()
file6 = open('6list', 'wb')
pickle.dump(ListSortedByNum[6], file6)
file6.close()
file7 = open('7list', 'wb')
pickle.dump(ListSortedByNum[7], file7)
file7.close()

#Test pickle
file7new = open('7list', 'rb')
list7new = pickle.load(file7new)
file7new.close()
print(list7new)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                