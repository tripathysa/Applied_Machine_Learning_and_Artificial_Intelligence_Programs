#Formulation of problem: The problem was break down into following components:
#1) Read the adjacent-states file and assign neighbours to all the 50 states.
#2) Read the Leagacy file and Assign given frequencies to given states.
#3) For choosing states, I took the states in order of their maximum neighbours to minimum neighbours which formulated as a most constraining variable and loop through the states
#in that order.
#4) For each state in given order in (3), assign a valid frequency, checking at each step if its neighbours have not the same frequency,
#and not changing the frequencies of state given in legacy constraints file.
#5) At each step, if no choice exists for a state, we call backtrack()
#6) Backtrack() calls each neighbours of the state one by one in step 5 and assign them a different frequency than previous and again check if any choice
#exists for that step.If a choice is found, break the  loop.
#7)While doing backtrack for a state, if a neighbour of that state returns no choices then call backtrack for that neighbour.

#How my program works:
#1) Program runs correctly assigning different values to all the states from its neighbours and h=keeping the values in legacy file intact.
#2) Program runs correctly for all the three legacy constraint files.
#3) Program  runs with 0 backtracks for legacy-constraints-1 file
#4) Program  runs with 0 backtracks for legacy-constraints-2 file
#5) Program  runs with 1 backtrack for legacy-constraints-3 file


#Problems and challenges Faced:
#1) Maintaining multiple dictionaries for neighbours, constraints and frequencies
#2) Loooping through Adjacent states and assign neighbours to each state was a challenge.
#3) In Backtrack function, changing frequencies of each neighbor and then again checking back the previous state was time taking.

#Analysis of program and scope of improvement:
#1)  The program works correctly for all given constraints that too, not with much time complexity,since backtracking is correctly implemented and
# COnstraints checking has been done meticulously.
#2) There is nuch scope for improvement as far as time complexity is concerned.Implementation wise, Ideally , variable can be selected with most constraining
#approach first ,then on clash, most constrained and for value, select least constraining value to optimize the program.Though the program used the most constraining approach for variable selection.
#3) I could have used fewer lists and dicts to lessen space complexity too.


import sys
import os
import collections
from collections import OrderedDict
from collections import defaultdict
import random
fileStatesName = 'adjacent-states'
fileInput=sys.argv[1]
listOfStates=[]
SortedListofStates=[]
freqList=[]
finalList=[]
StateFrequencies = {}
adjacentStates = {}
Frequencies= ['A', 'B', 'C', 'D']
backtrackCount=0
if os.stat(fileInput).st_size <= 1:
    dataFrequency=[]
else:
    with open(fileInput) as f:
        dataFrequency= f.readlines()
    for i, _ in enumerate(dataFrequency):
        dataFrequency[i] = dataFrequency[i].split()
    StateFrequencies=dict(dataFrequency)
with open(fileStatesName) as f:
    data = f.read().split()
    listOfStates=sorted(list(set(data)))
with open(fileStatesName) as f:
    dataEdges= f.readlines()
for i, _ in enumerate(dataEdges):
    dataEdges[i] = dataEdges[i].split()

for i, _ in enumerate(listOfStates):
    for j, _ in enumerate(dataEdges):
        if listOfStates[i] == dataEdges[j][0]:
            if len(dataEdges[j])>1:
                adjacencyList=[]
                adjacencyList=list(dataEdges[j])
                adjacencyList.remove(listOfStates[i])
                adjacentStates[listOfStates[i]] = adjacencyList
            else:
                adjacentStates[listOfStates[i]]=[]
#                StateFrequencies[listOfStates[i]] = random.choice(Frequencies)

orderDict = OrderedDict(sorted(adjacentStates.viewitems(), key=lambda x: len(x[1]),reverse=True))
SortedListofStates=orderDict.keys()
data=StateFrequencies.keys()
finalList = [x for x in SortedListofStates if x not in data]

def freqValid(state, freq):
    for adjstate in adjacentStates.get(state):
        adjacentStateFreq = StateFrequencies.get(adjstate)
        if adjacentStateFreq == freq:
            return False

    return True

def ValidFreq(state,listFreqs):
    if state in dict(dataFrequency).keys():
        return StateFrequencies[state]
    else:
        for freq in listFreqs:
            if freqValid(state, freq):
                return freq
def backtrack(state):
    global backtrackCount
    backtrackCount=backtrackCount+1
    datanextstates=adjacentStates[state]
    data4=[x for x in datanextstates if x not in dict(dataFrequency).keys()]
    data=[x for x in data4 if x in StateFrequencies.keys()]
    data1=[]
    for i, _ in enumerate(data):
        if StateFrequencies.has_key(data[i]):
            data1.extend(StateFrequencies[data[i]])
            D = defaultdict(list)
            for i,item in enumerate(data1):
                D[item].append(i)
            data2 = {k:v for k,v in D.items() if len(v)>1}
            list1=data2.values()
            list2=[item for sublist in list1 for item in sublist]
            j=0
            templistStates=[]

            while j<len(data1):
                if list2:
                    if j not in list2:
                        templistStates.append(data[j])
                else:
                    templistStates.append(data[j])
                j=j+1
            k=0
            while k<len(templistStates):
                q=ValidFreq(state,Frequencies)
                if q is None:

                    newfreqlist= [x for x in Frequencies if x != StateFrequencies[templistStates[k]]]
                    freq1=ValidFreq(templistStates[k],newfreqlist)
                    StateFrequencies[templistStates[k]]=freq1

                else:
                    StateFrequencies[state]=ValidFreq(state,Frequencies)
                    break



                k=k+1


def AssignFrequencies():
    global backtrackCount
    for state in finalList:
        assigned_freq=ValidFreq(state,Frequencies)
        datanextstates=adjacentStates[state]
        if assigned_freq is None:
            backtrack(state)
            for i, _ in enumerate(StateFrequencies.keys()):
                if StateFrequencies[StateFrequencies.keys()[i]] is None:
                    backtrack(StateFrequencies.keys()[i])

        else:
            StateFrequencies[state] = assigned_freq
    for key, value in collections.OrderedDict(sorted(StateFrequencies.items())).iteritems():
        temp = [key,value]
        freqList.append(temp)
    for i, _ in enumerate(freqList):
        print freqList[i][0] + "   " + str(freqList[i][1])
    file = open("results.txt", "w")
    for i, _ in enumerate(freqList):
        file.write(freqList[i][0] + "   " + str(freqList[i][1])+"\n")
    file.close()
    print "\n"+"Number of backtracks: " + str(backtrackCount)

AssignFrequencies()