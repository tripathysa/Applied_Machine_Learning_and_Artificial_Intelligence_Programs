#This program tries to classify the correct orientation of images given in test file
#Algorithms: 1) K-nearest neighbors 2) Neural Networks
#1) K-nearest Neighbors, we are calculating "Euclidean distance" between each test image with all the training images and taking
#specified k minimums amongst them which are called the k-neighbors of that test image.
# Then, Amongst the neighbors we select maximum occuring result as the final result for that test image.

#2) Neural Networks:We have implemented a feed forward-backpropagation neural network with 192 input neurons and 4 output neurons and hidden neurons are taken through
#console.We have used 'Numpy' library for the matrix operations.
#Initially random weights are assigned to each input node in range{0,1}
# Then, we have calculated the outputs in a range {0,1} through sigmoid function: 1/(1+e^(-x)). Calculating the delta to get the difference
# between given and actual labels i.e error.After getting error, we propagate backwards and again do the same process.For our program, this iteration is set to
# 5000 and error is printed after every 1000 iterations.


#Detailed analysis of th program in mentioned in the report.

import sys
import random
import math
import time
import operator
import itertools
import numpy as np

#NN Implementation Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:
def read_data_test_nn(fname):
    exemplars = []
    exemplars1=[]
    OpList=[]
    ImageNameList=[]
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        data=list(data)
        ImageNameList.append(data[0])
        if(data[1]=='0'):
            OpList.append([1,0,0,0])

        elif(data[1]=='90'):
            OpList.append([0,1,0,0])

        elif(data[1]=='180'):
            OpList.append([0,0,1,0])

        elif(data[1]=='270'):
            OpList.append([0,0,0,1])
        exemplars=[]
        for i in range(2,len(data)):
            exemplars.append(float(data[i]))
        data1=[float(j)/sum(exemplars) for j in exemplars]
        exemplars1.append(data1)
        del exemplars

    return exemplars1,OpList,ImageNameList
def read_data_nn(fname):
    exemplars = []
    exemplarsfinal=[]
    outputlist=[]
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        data=list(data)
        if(data[1]=='0'):
            outputlist.append([1,0,0,0])

        elif(data[1]=='90'):
            outputlist.append([0,1,0,0])

        elif(data[1]=='180'):
            outputlist.append([0,0,1,0])

        elif(data[1]=='270'):
            outputlist.append([0,0,0,1])
        exemplars=[]
        for i in range(2,len(data)):
            exemplars.append(float(data[i]))
        data1=[float(j)/sum(exemplars) for j in exemplars]
        exemplarsfinal.append(data1)
        del exemplars

    return exemplarsfinal,outputlist
class BackPropagationFeedForwardNetwork:
    #class members:
    layerCount=0
    shape=None
    weights=[]
    #class methods:
    def __init__(self,layerlength):
        #Network init
        self.layerCount=len(layerlength)-1
        self.shape=layerlength

        #input output data from last run
        self._Input=[]
        self._Output=[]

        # Create the weight lists
        for (l1,l2) in zip(layerlength[:-1],layerlength[1:]):
            self.weights.append(np.random.normal(scale=0.1,size=(l2,l1+1)))

    def classify(self,input):
        # run the network based on input data
        lnCases=input.shape[0]
        #clear the previous intermediate value list
        self.Input=[]
        self._Output=[]

        #Run it:
        for index in range(self.layerCount):
            #Determine layer Input
            if index==0:
                Input=self.weights[0].dot(np.vstack([input.T,np.ones([1,lnCases])]))
            else:
                Input=self.weights[index].dot(np.vstack([self._Output[-1],np.ones([1,lnCases])]))

            self._Input.append(Input)
            self._Output.append(self.sgm(Input))
        return self._Output[-1].T

    #Training Method:
    def TrainEpoch(self,input,target,trainingRate=0.2):
        #This method trains the network for one period of time
        delta=[]
        lnCases=input.shape[0]

        #First Run the network
        self.classify(input)
        #Calculate the deltas
        for index in reversed(range(self.layerCount)):
            if index==self.layerCount-1:
                #Compare to the output values
                output_delta=self._Output[index]-target.T
                error=np.sum(output_delta**2)
                delta.append(output_delta * self.sgm(self._Input[index],True))
            else:
                #Compare to the following layer's delta
                delta_pullback=self.weights[index+1].T.dot(delta[-1])
                delta.append(delta_pullback[:-1, :] * self.sgm(self._Input[index], True))
            #Compute Weight deltas
        for index in range(self.layerCount):
            delta_index=self.layerCount-1-index
            if index==0:
                Output=np.vstack([input.T,np.ones([1,lnCases])])
            else:
                Output=np.vstack([self._Output[index-1],np.ones([1,self._Output[index-1].shape[1]])])

            weightDelta=np.sum(\
                               Output[None,:,:].transpose(2,0,1) * delta[delta_index][None,:,:].transpose(2,1,0)\
                               ,axis=0)
            self.weights[index]-=trainingRate * weightDelta
        return error


    # Transfer Function
    def sgm(self,x,Derivative=False):
        if not Derivative:
            try:
                return 1/(1+math.e**(-x))
            except OverflowError:
                return float("inf")
        else:
            out=self.sgm(x)
            return out*(1-out)





def classifywithNN(train_file,test_file,hidden_count):
    nwInstance=BackPropagationFeedForwardNetwork((192,hidden_count,4))
    training_set_inputs,training_set_outputs=read_data_nn(train_file)
    lvInput = np.array(training_set_inputs)
    lvTarget = np.array(training_set_outputs)
    lnMax=800
    lnErr=1e-5
    print "\nTraining Neural Network in progress...\n"
    for i in range(lnMax+1):
        err=nwInstance.TrainEpoch(lvInput,lvTarget)
        if i%100==0:
            print ("Iteration{0}\tError:{1:0.6f}".format(i,err))
        if err<=lnErr:
            print("error converged  reached at iteration{0}".format(i))
            break

    #Display Output

    confusionMatrix = [[0 for x in range(4)] for x in range(4)]

    ListOp=['0','90','180','270']
    # Test the neural network with a new situation.
    print '\nTesting new Images for Classification...\n'
    test_set_inputs,test_set_outputs,Imagenames=read_data_test_nn(test_file)
    testInput = np.array(test_set_inputs)
    output=nwInstance.classify(testInput)
    print str(len(testInput)) + "length of test input\n"
    print str(len(output)) + "length of test output"
    file = open("nnet_output.txt", "w")
    for i in range(0,len(test_set_inputs)):
        given=str(ListOp[test_set_outputs[i].index(max(test_set_outputs[i]))])
        predicted=str(ListOp[output[i].tolist().index(max(output[i].tolist()))])
        if(given=='0' and predicted=='0'):
            confusionMatrix[0][0]=confusionMatrix[0][0]+1
        elif(given=='0' and predicted=='90'):
            confusionMatrix[0][1]=confusionMatrix[0][1]+1
        elif(given=='0' and predicted=='180'):
            confusionMatrix[0][2]=confusionMatrix[0][2]+1
        elif(given=='0' and predicted=='270'):
            confusionMatrix[0][3]=confusionMatrix[0][3]+1
        elif(given=='90' and predicted=='0'):
            confusionMatrix[1][0]=confusionMatrix[1][0]+1
        elif(given=='90' and predicted=='90'):
            confusionMatrix[1][1]=confusionMatrix[1][1]+1
        elif(given=='90' and predicted=='180'):
            confusionMatrix[1][2]=confusionMatrix[1][2]+1
        elif(given=='90' and predicted=='270'):
            confusionMatrix[1][3]=confusionMatrix[1][3]+1
        elif(given=='180' and predicted=='0'):
            confusionMatrix[2][0]=confusionMatrix[2][0]+1
        elif(given=='180' and predicted=='90'):
            confusionMatrix[2][1]=confusionMatrix[2][1]+1
        elif(given=='180' and predicted=='180'):
            confusionMatrix[2][2]=confusionMatrix[2][2]+1
        elif(given=='180' and predicted=='270'):
            confusionMatrix[2][3]=confusionMatrix[2][3]+1
        elif(given=='270' and predicted=='0'):
            confusionMatrix[3][0]=confusionMatrix[3][0]+1
        elif(given=='270' and predicted=='90'):
            confusionMatrix[3][1]=confusionMatrix[3][1]+1
        elif(given=='270' and predicted=='180'):
            confusionMatrix[3][2]=confusionMatrix[3][2]+1
        elif(given=='270' and predicted=='270'):
            confusionMatrix[3][3]=confusionMatrix[3][3]+1
        print('Original Orientation =' + given + ', Predicted Orientation =' + predicted)
        file.write(Imagenames[i] + "   " + predicted+"\n")
    file.close()
    countaccurate=0
    print '\nThe Confusion matrix after classification of all test images is below:'
    for i in range(0,4):
        print confusionMatrix[i]
        for j in range(0,4):
            if i==j:
                countaccurate=countaccurate+confusionMatrix[i][j]
    print "\n Percentage of correct prediction of orientation of test images" + "--> "+ str((countaccurate/float(len(test_set_inputs))) * 100.0)+"%"



#NN Implementation End >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:


#KNN Implementation Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:
def read_data(fname):
    exemplars = []
    listnames=[]
    file = open(fname, 'r');
    for line in file:
        data= tuple([w.lower() for w in line.split()])
        data=list(data)
        listnames.append(data[0])
        for j in range(1,len(data)):
            data[j]=int(data[j])
        data=tuple(data)
        exemplars+=[data]

    return exemplars,listnames

#calculate Euclidean Distance
def calculateDistance(set1, set2):
	distance = 0
	for x in range(2,len(set1)):
		distance += (set1[x] - set2[x])**2
	return distance

#Get K nearest neighbors
def getKNeighbors(trainingdata, testdata, k):
	ListDistances = []
	for i in range(0,len(trainingdata)):
		distance = calculateDistance(testdata, trainingdata[i])
		ListDistances.append((trainingdata[i], distance))
	neighbors = []
	ListDistances.sort(key=operator.itemgetter(1))
	for x in range(k):
		neighbors.append(ListDistances[x][0])
	return neighbors


def getMaximumLikelyOrientation(neighbors):
	neighborOrientation = {}
	for x in range(len(neighbors)):
		orientation = neighbors[x][1]
		if orientation in neighborOrientation:
			neighborOrientation[orientation] += 1
		else:
			neighborOrientation[orientation] = 1
	sortedOrientation= sorted(neighborOrientation.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedOrientation[0][0]

def GetaccuracyPercentage(test_data, classifications):
	correct = 0
	for x in range(len(test_data)):
		if test_data[x][1] == classifications[x]:
			correct += 1
	return (correct/float(len(test_data))) * 100.0

#best
def classifywithbest(train_file,test_file):
    confusionMatrix = [[0 for x in range(4)] for x in range(4)]
    print 'Learning Model...'
    train_data,ImageLabeltrain = read_data(train_file)
    test_data,ImageLabelTest = read_data(test_file)
    Classifications=[]
    file = open("best_output.txt", "w")
    for i in range(0,len(test_data)):
        neighbors = getKNeighbors(train_data, test_data[i], 10)
        result = getMaximumLikelyOrientation(neighbors)
        Classifications.append(result)
        given=str(test_data[i][1])
        predicted=str(result)
        if(given=='0' and predicted=='0'):
            confusionMatrix[0][0]=confusionMatrix[0][0]+1
        elif(given=='0' and predicted=='90'):
            confusionMatrix[0][1]=confusionMatrix[0][1]+1
        elif(given=='0' and predicted=='180'):
            confusionMatrix[0][2]=confusionMatrix[0][2]+1
        elif(given=='0' and predicted=='270'):
            confusionMatrix[0][3]=confusionMatrix[0][3]+1
        elif(given=='90' and predicted=='0'):
            confusionMatrix[1][0]=confusionMatrix[1][0]+1
        elif(given=='90' and predicted=='90'):
            confusionMatrix[1][1]=confusionMatrix[1][1]+1
        elif(given=='90' and predicted=='180'):
            confusionMatrix[1][2]=confusionMatrix[1][2]+1
        elif(given=='90' and predicted=='270'):
            confusionMatrix[1][3]=confusionMatrix[1][3]+1
        elif(given=='180' and predicted=='0'):
            confusionMatrix[2][0]=confusionMatrix[2][0]+1
        elif(given=='180' and predicted=='90'):
            confusionMatrix[2][1]=confusionMatrix[2][1]+1
        elif(given=='180' and predicted=='180'):
            confusionMatrix[2][2]=confusionMatrix[2][2]+1
        elif(given=='180' and predicted=='270'):
            confusionMatrix[2][3]=confusionMatrix[2][3]+1
        elif(given=='270' and predicted=='0'):
            confusionMatrix[3][0]=confusionMatrix[3][0]+1
        elif(given=='270' and predicted=='90'):
            confusionMatrix[3][1]=confusionMatrix[3][1]+1
        elif(given=='270' and predicted=='180'):
            confusionMatrix[3][2]=confusionMatrix[3][2]+1
        elif(given=='270' and predicted=='270'):
            confusionMatrix[3][3]=confusionMatrix[3][3]+1
        file.write(ImageLabelTest[i] + "   " + predicted+"\n")
        print('Original Orientation =' + str(test_data[i][1]) + ', Predicted Orientation =' + str(result))
    file.close()
    print '\nThe Confusion matrix after classification of all test images is below:'
    for i in range(0,4):
        print confusionMatrix[i]
    percentagecorrect=GetaccuracyPercentage(test_data, Classifications)
    print('\nPercentage of images correctly classified' +' -->'+ str(percentagecorrect) + '%\n')
#end Best
def classifyKNN(train_file,test_file,k):
    confusionMatrix = [[0 for x in range(4)] for x in range(4)]
    print 'Learning Model...'
    train_data,ImageLabeltrain = read_data(train_file)
    test_data,ImageLabelTest = read_data(test_file)
    Classifications=[]
    file = open("knn_output.txt", "w")
    for i in range(0,len(test_data)):
        neighbors = getKNeighbors(train_data, test_data[i], k)
        result = getMaximumLikelyOrientation(neighbors)
        Classifications.append(result)
        given=str(test_data[i][1])
        predicted=str(result)
        if(given=='0' and predicted=='0'):
            confusionMatrix[0][0]=confusionMatrix[0][0]+1
        elif(given=='0' and predicted=='90'):
            confusionMatrix[0][1]=confusionMatrix[0][1]+1
        elif(given=='0' and predicted=='180'):
            confusionMatrix[0][2]=confusionMatrix[0][2]+1
        elif(given=='0' and predicted=='270'):
            confusionMatrix[0][3]=confusionMatrix[0][3]+1
        elif(given=='90' and predicted=='0'):
            confusionMatrix[1][0]=confusionMatrix[1][0]+1
        elif(given=='90' and predicted=='90'):
            confusionMatrix[1][1]=confusionMatrix[1][1]+1
        elif(given=='90' and predicted=='180'):
            confusionMatrix[1][2]=confusionMatrix[1][2]+1
        elif(given=='90' and predicted=='270'):
            confusionMatrix[1][3]=confusionMatrix[1][3]+1
        elif(given=='180' and predicted=='0'):
            confusionMatrix[2][0]=confusionMatrix[2][0]+1
        elif(given=='180' and predicted=='90'):
            confusionMatrix[2][1]=confusionMatrix[2][1]+1
        elif(given=='180' and predicted=='180'):
            confusionMatrix[2][2]=confusionMatrix[2][2]+1
        elif(given=='180' and predicted=='270'):
            confusionMatrix[2][3]=confusionMatrix[2][3]+1
        elif(given=='270' and predicted=='0'):
            confusionMatrix[3][0]=confusionMatrix[3][0]+1
        elif(given=='270' and predicted=='90'):
            confusionMatrix[3][1]=confusionMatrix[3][1]+1
        elif(given=='270' and predicted=='180'):
            confusionMatrix[3][2]=confusionMatrix[3][2]+1
        elif(given=='270' and predicted=='270'):
            confusionMatrix[3][3]=confusionMatrix[3][3]+1
        file.write(ImageLabelTest[i] + "   " + predicted+"\n")
        print('Original Orientation =' + str(test_data[i][1]) + ', Predicted Orientation =' + str(result))
    file.close()
    print '\nThe Confusion matrix after classification of all test images is below:'
    for i in range(0,4):
        print confusionMatrix[i]
    percentagecorrect=GetaccuracyPercentage(test_data, Classifications)
    print('\nPercentage of images correctly classified' +' -->'+ str(percentagecorrect) + '%\n')
#KNN Implementation End >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:
if __name__== "__main__":
    starttime=time.time()
    if len(sys.argv) < 4 or len(sys.argv) > 5 :
        print "Usage: python orient.py training_file test_file  knn/nnet/best k/hiddencount"
        sys.exit()
    train_file= sys.argv[1]
    test_file= sys.argv[2]
    algorithm= sys.argv[3]
    if len(sys.argv)==5 and algorithm=='knn':
        if sys.argv[4]=='0':
            print "Value of k can't be zero"
            sys.exit()
        k = int(sys.argv[4])
        classifyKNN(train_file,test_file,k)
    elif len(sys.argv)==5 and algorithm=='nnet':
        if sys.argv[4]=='0':
            print "Value of hidden count can't be zero"
        hiddencount=int(sys.argv[4])
        classifywithNN(train_file,test_file,hiddencount)
    elif len(sys.argv)==4 and algorithm=='best':
        classifywithbest(train_file,test_file)
    print("\n--- (Program time in minutes) --- " + str((time.time() - starttime)/60))




