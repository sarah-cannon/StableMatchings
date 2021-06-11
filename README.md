# StableMatchings
Code for investigating counting and sampling of range-restricted stable matchings

3list (4list, 5list, 7list) is a list containing all preferences lists that result in 3 (4, 5, 7) stable matchings. These are for the case where there are 4 people on each side and range restrictions of size 3 on both sides.

3list_asym34 etc. are the same, but when one side has range 3 restrictions and the other side has rage 4 restrictions (that is, no range restrictions)

Size4code is the python file that produced all the above lists

MakeRotationPosets is the code used to find all the different possible state spaces that results from a given list of preference lists; that is what generated the images I showed in our 6/11/21 meeting. 

Size5code was an attempt to generate the same lists as above when there are 5 people on each side.  I was able to generate all possible preference lists for the A side and all possible preference lists for the B side, these are stored in Size5_range33_AllAPrefLists and Size5_range33_AllBPrefLists.  However, the code that takes and A preference list, a B preference lists, and sees how manys table matchings results, did not finish running (and based on my calculation, would take about 2 months to run. 

Places for improvements: 
1. Instead of generating all preference lists for size 5 matchnigs, only use those that come from 'cascades,' since we now that's the only interesting case. 
2. Improving the way the code finds all stable matchings for given preference lists: currently it looks at all possible matchings, and for each matching looks at all (i,j) pairs and determines if it's an unstable pair.  I suspect this could be done much faster! 
