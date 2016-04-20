from collections import namedtuple
import sys
""" 
Program to find the correct matches for m given people, n products and p streets
Aim is to find a solution which satifies the goal node criteria which is in not a node but a set of conditions 
which must NOT be met
"""

""" Given: 
    Names of 5 people(customers)        -   customer[]  = "F","G","H","I","J";
    Names of 5 products(orders)         -   order[]     = "A","B",C","D","E";
    Names of 5 addresses(streets)       -   street[]    = "K","L",M","N","O";
    Negative conditions/constraints each of them not to be met
    
    Approach:
        There are two different types of constraints we see:

        (1) First is direct where negative conditions are provided.
        Those which DO NOT go together are 7 in number (4th and 7th are deduced based on others):
                        1 | 2 | 3 | 4 | 5 | 6 | 7
        Customer    - F | G | H | I |   |   |
        Order       - D |   |   | B | E | A | E
        Street      -   | K | O |   | M | M | N

        (2) Second type is rules to be applied dynamically after which the answers will be obtained.
        Principle:
        We approach by double negativity which leads to positive outcome:
        �(�x) = x
        Here, To every state given out by the successor function, the negative rules of (2) are applied to get a state satisfying negative criteria as in (1).
        This ensures that there is only one goal state. Not every state satifies all the negative criteria.
"""
#define a start state - these lists will be modified during the course of execution to obtain successor states
customer    = ['I','G','J','H','F']
order       = ['D','A','E','C','B']
street      = ['L','M','N','O','K']

#Reality     = [['F','D'],['G','K'],['E','N'],['A','M'],['H','O'],['I','B'],['E','M']]

#list contains the negative constraints obtained to check if it is the goal state
negConsList = [[]]

#State dynamically populated to avoid symmetric goal states while printing
symmetryCheckCustomer=[]
symmetryCheckOrder=[]
symmetryCheckStreet=[]

#Global variable to verify if a symmetric goal is already printed
isAlreadyPrinted = False
#helper function for obtaining next state
def ShiftArray(num):
    if(num==1):
        tempnum = customer[0]
        customer[0] = customer[1]
        customer[1] = customer[2]
        customer[2] = customer[3]
        customer[3] = customer[4]
        customer[4] = tempnum

    elif(num==2):
        tempnum = order[0]
        order[0] = order[1]
        order[1] = order[2]
        order[2] = order[3]
        order[3] = order[4]
        order[4] = tempnum

    elif(num==3):
        tempnum = street[0]
        street[0] = street[1]
        street[1] = street[2]
        street[2] = street[3]
        street[3] = street[4]
        street[4] = tempnum
    return

#funciton to list the erraneous conditions based on current state
def addToObtainedErrList(str1, str2):
    negConsList.append([str1,str2])
    return

#function to get person name based on input order/street
def getPerson(str, num):
    if(num == 2):
        for i in xrange(0,5):
            if(order[i] == str):
                return customer[i]
    if(num == 3):
        for i in xrange(0,5):
            if(street[i] == str):
                return customer[i]

#function to get order name based on input customer/street
def getOrder(str, num):
    if(num == 1):
        for i in xrange(0,5):
            if(customer[i] == str):
                return order[i]
    if(num == 3):
        for i in xrange(0,5):
            if(street[i] == str):
                return order[i]

#function to get street name based on input order/customer
def getStreet(str, num):
    if(num == 2):
        for i in xrange(0,5):
            if(order[i] == str):
                return street[i]
    if(num == 1):
        for i in xrange(0,5):
            if(customer[i] == str):
                return street[i]

#following function lists the erraneous combinations to find out if the mistakes were the same as which happened in reality
def checkByRules():#returns true if all the conditions satisfy for Reality
    #clear error list
    negConsList[:] = []
    #print "cleared negConsList:"
    #print (negConsList)
    #person who ordered C got B
    Pc = getPerson('C', 2)#2 stands for order
    addToObtainedErrList(Pc,'B')

    #person who ordered B got I's order
    Pb = getPerson('B', 2)#2 stands for order
    Oi = getOrder('I', 1)#1 stands for person
    addToObtainedErrList(Pb, Oi)

    #order suposed to be at K went to L
    Ok = getOrder('K', 3)#3 stands for street
    addToObtainedErrList(Ok,'L')

    #J received H's order
    Oh = getOrder('H', 1)
    addToObtainedErrList('J', Oh)

    #Person who ordered E got order at M
    Pe = getPerson('E', 2)
    Om = getOrder('M', 3)
    addToObtainedErrList(Pe, Om)

    #validate against main error list - 
    retVal = False
    if (['F','D'] in negConsList) and (['I','B'] in negConsList):
        retVal = True
    return retVal

#check if next state is the goal
def checkNextGoal():
    if(isGoal()==True):
        printGoal()
    else:
        for c in xrange(0,5):
            for o in xrange(0,5):
                for s in xrange(0,5):
                    ShiftArray(3)
                    if (isGoal()==True):                    
                        printGoal()
                ShiftArray(2)
                if (isGoal()==True):
                    printGoal()
            ShiftArray(1)
            if (isGoal()==True):
                printGoal()
    return

#helper function
def isCombination(cust, ord, strt):
    for i in xrange(0,5):
        if ((customer[i] == cust and order[i] == ord) or (customer[i] == cust and street[i] == strt) or (street[i] == strt and order[i] == ord)):
            return True
    return False  


#if atleast one of the combinations is met, the state is not a goal state
#returns true if atleast one of the below combinations is met
def checkByVariables():
    b1 = isCombination('F','D','')
    b2 = isCombination('G','','K')
    b3 = isCombination('','E','N')
    b4 = isCombination('','A','M')
    b5 = isCombination('H','','O')
    b6 = isCombination('I','B','')
    b7 = isCombination('','E','M')
    if(b1 or b2 or b3 or b4 or b5 or b6 or b7):
        return True
    return False

#main method to check for goal criteria
def isGoal():
    #checkByVariables() will check for direct negative constraints
    #checkByRules() will dynamically apply rules and verify for negative constraints

    if(checkByVariables() == False):    #even if this condition is satisfied, we have to check if the other rules are followed
        if(checkByRules() == True):     #applies rules and verifies if this is the goal state
            for z in xrange(0,5):
                symmetryCheckCustomer.insert(z, customer[z])
                symmetryCheckOrder.insert(z,order[z])
                symmetryCheckStreet.insert(z,street[z])
            return True
    return False


#function to check for symmetricity
def isSymmetricToGoal():
    if len(symmetryCheckCustomer)>0:
        varTemp1 = customer[0]
        varTemp2 = order[0]
        varTemp3 = street[0]
        for x in xrange(0,5):
            if symmetryCheckCustomer[x] == varTemp1:
                if symmetryCheckOrder[x] == varTemp2:
                    if symmetryCheckStreet[x] == varTemp3:
                        if isAlreadyPrinted==False:
                            return False
                        else:
                            return True
    return False
#function to print goal
def printGoal():
    global isAlreadyPrinted
    if isSymmetricToGoal() == False:#if not symmetric to the goal previously obtained, print it
       if isAlreadyPrinted == False:  
            print "Found Goal"
            for x in xrange(0,5):
                print(customer[x]),
            print ""
            for x in xrange(0,5):
                print(order[x]),
            print ""
            for x in xrange(0,5):
                print(street[x]),
            isAlreadyPrinted = True
    return

#execution starts here
checkNextGoal()
print ""
print ""
print "END"
print ""