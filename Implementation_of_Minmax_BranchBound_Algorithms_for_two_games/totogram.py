#The program works for all the depths,even > 7 and finally gives the totogram score and the optimal arrangement of nodes in the tree.
#The programming logic is basically a kind of branch and bound in which we split the elements of the list into 3,6,12,24 sublists according to the depth
#and then compare the level above nodes with each sublist and take the minimum value.
# 1)we deduce the number of elements based on depth and put it in a list.
#2) Since we know by brute force that we should start the tree with the median because it keeps the tree balanced.
#3) Then we divide the list into 3 equal numbered sublists.
#4) Then subtract the root element with all the elements of sublist and take the one with minimum difference.This way we get 3 nodes for level 2.
#5) Repeat the above process again by dividing the list into 6,12,24 equal sublists and taking minimums.

#For Input depth= 3:
#Output is:
#3
#6 3 5 8 1 2 4 7 9 10
#Time Elapsed:--- 0.0160000324249 seconds ---

#For Input depth= 4:
#Output is:
#5
#12 7 11 16 3 6 10 13 17 20 1 2 4 5 8 9 14 15 18 19 21 22
#Time Elapsed: --- 0.000999927520752 seconds ---

#For Input depth= 5:
#Output is:
#9
#24 15 23 32 7 14 22 25 33 40 3 6 10 13 18 21 26 29 34 37 41 44 1 2 4 5 8 9 11 12 16 17 19 20 27 28 30 31 35 36 38 39 42 43 45 46
#Time Elapsed: --- 0.00100016593933 seconds ---

#For Input depth= 6:
#Output is:
#17
#48 31 47 64 15 30 46 49 65 80 7 14 22 29 38 45 50 57 66 73 81 88 3 6 10 13 18 21 25 28 34 37 41 44 51 54 58 61 67 70 74 77 82 85 89 92 1 2 4 5 8 9 11 12 16 17 19 20 23 24 26 27 32 33 35 36 39 40 42 43 52 53 55 56 59 60 62 63 68 69 71 72 75 76 78 79 83 84 86 87 90 91 93 94
#Time Elapsed: --- 0.00100016593933 seconds ---

#For Input depth= 7:
#Output is:
#33
#96 63 95 128 31 62 94 97 129 160 15 30 46 61 78 93 98 113 130 145 161 176 7 14 22 29 38 45 53 60 70 77 85 92 99 106 114 121 131 138 146 153 162 169 177 184 3 6 10 13 18 21 25 28 34 37 41 44 49 52 56 59 66 69 73 76 81 84 88 91 100 103 107 110 115 118 122 125 132 135 139 142 147 150 154 157 163 166 170 173 178 181 185 188 1 2 4 5 8 9 11 12 16 17 19 20 23 24 26 27 32 33 35 36 39 40 42 43 47 48 50 51 54 55 57 58 64 65 67 68 71 72 74 75 79 80 82 83 86 87 89 90 101 102 104 105 108 109 111 112 116 117 119 120 123 124 126 127 133 134 136 137 140 141 143 144 148 149 151 152 155 156 158 159 164 165 167 168 171 172 174 175 179 180 182 183 186 187 189 190
#Time Elapsed: --- 0.0019998550415 seconds ---


#Earlier one more approach we followed which gave sub-optimal solution.
#:1) Calculate no of nodes based on depth and store it in a list 2) Extract middle numbers in a geometric progression
#starting from 3 with a multiplication factor of 2 like 3,6,12 etc. and assign it to another list.We finally return this list as output.
#For calculating the final totogram cost we know that the last level 1st node is 1(by brute force) and since 1 is the minimum cost node,the edge
#connected to it will give the final cost.Like at depth 3, arrangement is [5, 4, 6, 7, 1, 2, 3, 8, 9, 10] cost is 4-1=3
# at depth 4 : [11, 10, 12, 13, 7, 8, 9, 14, 15, 16, 1, 2, 3, 4, 5, 6, 17, 18, 19, 20, 21, 22] cost is 7-1=6

#the program is tested at all inputs and handles the default error conditions.
import sys
import time
import math
#start_time = time.time()
ListOpen=[]
ListFinal=[]
NumberElements=0
if sys.argv[1]!="":
    depth=int(sys.argv[1])
SubtractedList=[]
fringe=[]
fringe1=[]
fringe2=[]
fringe3=[]
fringe4=[]
ScoreList=[]
#Main function which calculates the score and optimal arrangement
def WinTotoGram(depth):
    if depth<0:
        return "Please pass valid depth value"
    if depth==0:
        return "No Nodes"
    if depth==1:
        return 1
    if depth==2:
        print 2
        return "2 1 3 4"
    NumberElements=int(1+ 3*(math.pow(2,(depth-1))-1))
    for i in xrange(1,NumberElements+1, 1):
        ListOpen.append(i)

    ListFinal.append([ListOpen.pop((NumberElements/2))])
    data =[ListOpen[x:x+len(ListOpen)/3] for x in xrange(0, len(ListOpen), len(ListOpen)/3)]
    for i in xrange(0,len(data),1):
        SubtractedList=[abs(x - ListFinal[0][0]) for x in data[i]]
        ScoreList.append([min(SubtractedList)])
        fringe.append(data[i][SubtractedList.index(min(SubtractedList))])
        ListOpen.remove(data[i][SubtractedList.index(min(SubtractedList))])
        del SubtractedList[:]
    ListFinal.append(fringe)
    if len(ListOpen)==6:
        ListFinal.append(ListOpen)
        Finalscore=max([item for sublist in ScoreList for item in sublist])
        print Finalscore
        del ScoreList[:]
        Finalscore=""
        dataToto=[item for sublist in ListFinal for item in sublist]
        #print("--- %s seconds ---" % (time.time() - start_time))
        return ' '.join(map(str, dataToto))
    k=6
    increment=1
    while True:
        datanext =[ListOpen[x:x+len(ListOpen)/k] for x in xrange(0, len(ListOpen), len(ListOpen)/k)]
        counter=0
        j=0
        while counter<len(datanext):
            if counter%2==0 and counter!=0:
                j=j+1
            SubtractedList=[abs(x - ListFinal[increment][j]) for x in datanext[counter]]
            ScoreList.append([min(SubtractedList)])
            fringe1.append(datanext[counter][SubtractedList.index(min(SubtractedList))])
            ListOpen.remove(datanext[counter][SubtractedList.index(min(SubtractedList))])
            del SubtractedList[:]
            counter=counter+1
        ListFinal.append(fringe1)
        if len(ListOpen)%12==0:
            ListFinal.append(ListOpen)
            Finalscore=max([item for sublist in ScoreList for item in sublist])
            print Finalscore
            del ScoreList[:]
            Finalscore=""
            dataToto=[item for sublist in ListFinal for item in sublist]
            #print("--- %s seconds ---" % (time.time() - start_time))
            return ' '.join(map(str, dataToto))
        k=k*2
        increment=increment+1
        del datanext[:]

print WinTotoGram(depth)

