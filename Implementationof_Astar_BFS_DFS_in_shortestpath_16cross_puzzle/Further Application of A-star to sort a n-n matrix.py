#The idea for this question was to have a heuristics like distance of each element from the corresponding one n goal state.For that we took heuristics as
#GoalRowNumber-PresentRowNumber + GoalColumnNumber-PresentColumnNumber
#We made four functions moveColumnUp,moveColumnDown,moveRowLeft,MoveRowDown to expand our possibilities
#Preparing a list with the start state, Calculate Heuristics of the nodes in openstate and take the minimum heuristic node for expansion and then
# Apply 4 functions to expand the search states, iterate through the state space.
#Tested on inputs:like
#13 6 2 3
#4 10 7 8
#5 14 11 12
#9 1 15 16

#13 1 2 3
#4 6 7 8
#5 10 11 12
#9 14 15 16

#8 2 15 4
#9 5 6 3
#13 10 7 12
#1 14 11 1


#1 2 15 4
#8 5 6 3
#9 10 7 12
#13 14 11 16


#13 1 2 3
#4 6 7 8
#5 10 11 12
#9 14 15 16


import collections
import copy
import sys
GoalState=[]
BoardData=[]
InputList=[]
itemFvalueList=[]
TraversedPath=[]
SequenceMoves=[]
Input_Board_File=sys.argv[1]
with open(Input_Board_File) as f:
    BoardData = f.readlines()
#Formatting Input in a list split by whitespace.
for i, _ in enumerate(BoardData):
    BoardData[i]=BoardData[i].split()

InputList=[BoardData]
#Assigning Goal State which will be frequently used for comparison with present states.
GoalState.append([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '16']])
#Function Search Start
def Astar(data):
    ListOpen = []
    ListOpen = InputList[:]
    Iteration=0
    while ListOpen:
        gValue=Iteration
        if(Iteration==0):
           if ListOpen[0] == GoalState[0]:
               return ListOpen[0]
        itemFvalueList.append(CalculateHeuristics(ListOpen))
        path = ListOpen.pop(itemFvalueList[0].index(min(itemFvalueList[0])))
        TraversedPath.append(path)
        if path == GoalState[0]:
            return path
        else:
            if(Iteration!= 0):
                #Print in format #R1,D2 etc
                print SequenceMoves[itemFvalueList[0].index(min(itemFvalueList[0]))]
                SequenceMoves.pop(itemFvalueList[0].index(min(itemFvalueList[0])))
                #Expand nodes
            ListOpen.extend(moveColumnUp(path,TraversedPath))
            ListOpen.extend(moveColumnDown(path,TraversedPath))
            ListOpen.extend(moveRowLeft(path,TraversedPath))
            ListOpen.extend(moveRowRight(path,TraversedPath))
        del itemFvalueList[:]
        Iteration=Iteration+1

def moveColumnDown(data,TraversedPath):
    TempList = copy.deepcopy(data)
    ListAdd=[]
    for n in xrange(0, 4, 1):
        temp=data[0][n]
        TempList[0][n]=data[3][n]
        TempList[3][n]=data[2][n]
        TempList[2][n]=data[1][n]
        TempList[1][n]=temp
        ListAdd.append(TempList)
        SequenceMoves.append("D"+str(n))
        if(CalculateHeuristics([TempList])[0]==0):
            print "D",n
            for node in TraversedPath:
             print node
            print GoalState[0]
            sys.exit()

        else:
            TempList = copy.deepcopy(data)
    return ListAdd

def moveColumnUp(data,TraversedPath):
    TempList = copy.deepcopy(data)
    ListAdd=[]
    for n in xrange(0, 4, 1):
         temp=data[3][n]
         TempList[3][n]=data[0][n]
         TempList[0][n]=data[1][n]
         TempList[1][n]=data[2][n]
         TempList[2][n]=temp
         ListAdd.append(TempList)
         SequenceMoves.append("U"+str(n))
         if(CalculateHeuristics([TempList])[0]==0):
             print "U",n
             for node in TraversedPath:
                 print node
             print GoalState[0]
             sys.exit()
         else:
            TempList = copy.deepcopy(data)
    return ListAdd

def moveRowRight(data,TraversedPath):
    TempList = copy.deepcopy(data)
    ListAdd=[]
    for n in xrange(0, 4, 1):
        temp=data[n][0]
        TempList[n][0]=data[n][3]
        TempList[n][3]=data[n][2]
        TempList[n][2]=data[n][1]
        TempList[n][1]=temp
        ListAdd.append(TempList)
        SequenceMoves.append("R"+str(n))
        if(CalculateHeuristics([TempList])[0]==0):
            print "R",n
            for node in TraversedPath:
                print node
            print GoalState[0]
            sys.exit()
        else:
            TempList = copy.deepcopy(data)
    return ListAdd
def moveRowLeft(data,TraversedPath):
    TempList = copy.deepcopy(data)
    ListAdd=[]
    for n in xrange(0, 4, 1):
        temp=data[n][3]
        TempList[n][3]=data[n][0]
        TempList[n][0]=data[n][1]
        TempList[n][1]=data[n][2]
        TempList[n][2]=temp
        ListAdd.append(TempList)
        SequenceMoves.append("L"+str(n))
        if(CalculateHeuristics([TempList])[0]==0):
            print "L",n
            for node in TraversedPath:
                print node
            print GoalState[0]
            sys.exit()

        else:
            TempList = copy.deepcopy(data)

    return ListAdd


def CalculateHeuristics(ListOpen):
    dataList=[]
    heuristicsValue=0
    for m, _ in enumerate(ListOpen):
        for n, _ in enumerate(ListOpen[m]):
            for p, _ in enumerate(ListOpen[m][n]):
                PresentColumnNumber=p
                PresentRowNumber=n
                if ListOpen[m][n][p]== '16':
                    GoalRowNumber=3
                    GoalColumnNumber=3
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '15':
                    GoalRowNumber=3
                    GoalColumnNumber=2
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '14':
                    GoalRowNumber=3
                    GoalColumnNumber=1
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '13':
                    GoalRowNumber=3
                    GoalColumnNumber=0
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '12':
                    GoalRowNumber=2
                    GoalColumnNumber=3
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '11':
                    GoalRowNumber=2
                    GoalColumnNumber=2
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '10':
                    GoalRowNumber=2
                    GoalColumnNumber=1
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '9':
                    GoalRowNumber=2
                    GoalColumnNumber=0
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '8':
                    GoalRowNumber=1
                    GoalColumnNumber=3
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '7':
                    GoalRowNumber=1
                    GoalColumnNumber=2
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '6':
                    GoalRowNumber=1
                    GoalColumnNumber=1
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '5':
                    GoalRowNumber=1
                    GoalColumnNumber=0
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '4':
                    GoalRowNumber=0
                    GoalColumnNumber=3
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '3':
                    GoalRowNumber=0
                    GoalColumnNumber=2
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '2':
                    GoalRowNumber=0
                    GoalColumnNumber=1
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
                if ListOpen[m][n][p]== '1':
                    GoalRowNumber=0
                    GoalColumnNumber=0
                    heuristicsValue+= abs(GoalRowNumber - PresentRowNumber) + abs(GoalColumnNumber - PresentColumnNumber)
        dataList.append(heuristicsValue)
        heuristicsValue=0
    return dataList

print Astar(InputList)