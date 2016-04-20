###################################
# CS B551 Fall 2015, Assignment #5
#
# Saurabh Tripathy- saurtrip
# ShreeHarsha S- sridhash
#
# (Based on skeleton code by D. Crandall)
#
#
####
#Report:
#Approach
# 1)
#   1)For setting up the training data, we have calculated Initial probabilities as how many times each tag is occuring as first word of the sentence
#, transition probabilities as how many times the duplets noun-verb, verb-verb are occuring in the corpus and emission probabilities as how many times a word is appearing as
#each tag.

#  2) For the naive approach, we have returned tag for each word in a sentence as max(P(tag(i)|word)) meaning if a word occurs mostly as verb in the
# training corpus then return verb as result.

#  3) For viterbi, we have followed the formula, like Emission[prev,next]*max[max favourable probabillity calculated for previous word*Transition of prev|next tag]

#  4) For MCMC,we are generating samples like taking initial sample as tag 'noun' for all the words in a sentence the changing one tag at a time with its most suitable tag.
#decided by probability TransitionAB*TransitionBC*EmissionB(Noun,Verb,......).Thus we are generating samples and adding only distinct samples to the list.
#Then we are returning last five samples from the list but generating more than 500 Here only we are storing most likely tag of the words for Max Marginal Algorithm.

#  5) For max marginal algorithm, since we already calculated, the most likely tag for each word in step 4 MCMC, we just need to search through the dictionary created in step 4 and print the most likely tag.

#  6) For the best algorithm, we have built on our naive strategy in which we have handled a scenario that when a key is not found in the corpus like we found "Nick's"
# as one such key then predict its tag by calcuating the maximum transition prbability with the tag preceding the word.Also, if equally suitable tags are found,we are
#comparing their transition probabilities individually with the previous tag.

# 7) For calculating the posterior probabilities, we calculated Initial probability + Product(Emissions for each tag) + Product(Transitions for each duplets of tags in t
# the sentence)

#2) Here are the results of evaluation with bc.test file.

# The program runs in around 40 secs for bc.test.tiny input file and around 4 minutes for bc.test file.

#Output:

#Here is the final result after running the code for bc.test file
# So far scored 2000 sentences with 29442 words.
#               Words correct:     Sentences correct:
#0. Ground truth:      100.00%              100.00%
#       1. Naive:       92.15%               39.25%
#     2. Sampler:       81.82%                0.55%
#3. Max marginal:       90.31%               33.55%
#         4. MAP:       88.87%               27.00%
#        5. Best:       92.15%               39.25%

#Problems faced/design decisions:
#1) In viterbi, if there is a key which is not found in the corpus like "Nick's' then all its probabilities became 0 at that stage.hence for the successive stages also
#the products became 0 and efficiency was really low. For this we assigned a realtively lower probability to each tag not found.

#2) Some sentences were really short like only "." in a sentence, so it generated little number of samples.So needed to handle when we were printing 5 samples as it had less than 5 samples.

#3) Earlier we started with calculating Emission probabilities of the words present in the test file searrching in training corpus which was making the program
#stalled due to the nested loops in the two data structures in test and train.Then we calculated Emission for each word in the training file only thus avoiding nesting.

#   Sampling is taking much time since we are generating multiple samples and calculating emission of each word in the sample for the max marginal.Thought of calculating emission
#  of samples in the training function onlyvfor each sentence in the test but was left with less time to recompute.

#   Got a lot of division by error exceptions which later got handled by adding a very small number to the probabilities.

# Viterbi,MCMC and setting training data was entirely based on playing with indices,so, struggled a lot when a error used to come and it was difficult to debug because
#of large training file.


####
from __future__ import division
import random
import math
from collections import defaultdict


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.InitialProbabilitiesList = {}
        self.TransmissionProbabilities = {}
        self.TransmissionProbabilities = defaultdict(lambda: [0,0,0,0,0,0,0,0,0,0,0,0],self.TransmissionProbabilities)
        self.EmissionProbablities={}
        self.ViterbiSequence={}
        self.ViterbiSequence = defaultdict(lambda: [0,0,0,0,0,0,0,0,0,0,0,0],self.ViterbiSequence)
        self.PartsofSpeechList=['verb','noun','det','adj','pron','conj','adv','.','adp','num','x','prt']
        self.ADJcount,self.ADVcount,self.ADPcount,self.CONJcount,self.DETcount,self.nouncount,self.NUMcount,self.PRONcount,self.VERBcount,self.Xcount,self.Punctcount,self.PRTcount=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.EmissionProbSample={}
        self.EmissionProbSample = defaultdict(lambda: [0,0,0,0,0,0,0,0,0,0,0,0],self.EmissionProbSample)


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        initprob=0.000000001
        finalLogProb=0
        productTransitionProbs=0.000000001
        productEmissionProbs=0.000000001
        for i in range(0,12):
            if label[0]==self.PartsofSpeechList[i]:
                initprob=initprob+self.InitialProbabilitiesList[self.PartsofSpeechList[i]]
        for i in range(0,len(sentence)-1):
            for k in range(0,12):
                if (label[i+1]==self.PartsofSpeechList[k]):
                    productTransitionProbs=(self.TransmissionProbabilities[label[i]][k]+.000001)*productTransitionProbs
        for j in range(0,len(sentence)):
            for k in range(0,12):
                if (sentence[j]==self.PartsofSpeechList[k]):
                    productEmissionProbs=productEmissionProbs*(self.EmissionProbablities[sentence[j]][k]+.000001)
        finalLogProb= math.log(initprob+0.00001)+math.log(productEmissionProbs)+math.log(productTransitionProbs)
        return finalLogProb
    # Do the training!
    #
    def train(self, data):
        countNounfirstword,countADJfirstword,countADVfirstword,countADPfirstword,countCONJfirstword,countDETfirstword,countNUMfirstword,countPRONfirstword,countVERBfirstword,countXfirstword,countPunctuationfirstword,countPRTfirstword=[0,0,0,0,0,0,0,0,0,0,0,0]
#        self.TestInputData=read_data(bc.test.tiny)
        for i in range(0, len(data)):

            self.ADJcount=self.ADJcount+data[i][1].count('adj')
            self.ADVcount=self.ADVcount+data[i][1].count('adv')
            self.ADPcount=self.ADPcount+data[i][1].count('adp')
            self.CONJcount=self.CONJcount+data[i][1].count('conj')
            self.DETcount=self.DETcount+data[i][1].count('det')
            self.nouncount=self.nouncount+data[i][1].count('noun')
            self.NUMcount=self.NUMcount+data[i][1].count('num')
            self.PRONcount=self.PRONcount+data[i][1].count('pron')
            self.VERBcount=self.VERBcount+data[i][1].count('verb')
            self.Xcount=self.Xcount+data[i][1].count('x')
            self.Punctcount=self.Punctcount+data[i][1].count('.')
            self.PRTcount=self.PRTcount+data[i][1].count('prt')
            if(data[i][1][0].upper()=='ADJ'):
                countADJfirstword=countADJfirstword+1
            elif(data[i][1][0].upper()=='ADV'):
                countADVfirstword=countADVfirstword+1
            elif(data[i][1][0].upper()=='ADP'):
                countADPfirstword=countADPfirstword+1
            elif(data[i][1][0].upper()=='CONJ'):
                countCONJfirstword=countCONJfirstword+1
            elif(data[i][1][0].upper()=='DET'):
                countDETfirstword=countDETfirstword+1
            elif(data[i][1][0].upper()=='NOUN'):
                countNounfirstword=countNounfirstword+1
            elif(data[i][1][0].upper()=='NUM'):
                countNUMfirstword=countNUMfirstword+1
            elif(data[i][1][0].upper()=='PRON'):
                countPRONfirstword=countPRONfirstword+1
            elif(data[i][1][0].upper()=='VERB'):
                countVERBfirstword=countVERBfirstword+1
            elif(data[i][1][0].upper()=='X'):
                countXfirstword=countXfirstword+1
            elif(data[i][1][0].upper()=='.'):
                countPunctuationfirstword=countPunctuationfirstword+1
            elif(data[i][1][0].upper()=='PRT'):
                countPRTfirstword=countPRTfirstword+1
        #Calculation of Initial probabilities of each part of speech tag.
        self.InitialProbabilitiesList['adj']=float(countADJfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['adv']=float(countADVfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['adp']=float(countADPfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['conj']=float(countCONJfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['det']=float(countDETfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['noun']=float(countNounfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['num']=float(countNUMfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['pron']=float(countPRONfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['verb']=float(countVERBfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['x']=float(countXfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['.']=float(countPunctuationfirstword)/float(len(data))+0.00000000001
        self.InitialProbabilitiesList['prt']=float(countPRTfirstword)/float(len(data))+0.00000000001

        #Calculation of Transition probabilities of each part of speech tag.

        for i in range(0, len(data)):
            for j in xrange(0,len(data[i][1])-1):
                for k in range(0,len(self.PartsofSpeechList)):
                    if (data[i][1][j]==self.PartsofSpeechList[k]):
                        if (data[i][1][j+1]=="verb"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][0]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][0]+1
                        elif (data[i][1][j+1]=="noun"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][1]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][1]+1
                        elif (data[i][1][j+1]=="det"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][2]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][2]+1
                        elif (data[i][1][j+1]=="adj"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][3]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][3]+1
                        elif (data[i][1][j+1]=="pron"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][4]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][4]+1
                        elif (data[i][1][j+1]=="conj"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][5]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][5]+1
                        elif (data[i][1][j+1]=="adv"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][6]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][6]+1
                        elif (data[i][1][j+1]=="."):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][7]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][7]+1
                        elif (data[i][1][j+1]=="adp"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][8]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][8]+1
                        elif (data[i][1][j+1]=="num"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][9]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][9]+1
                        elif (data[i][1][j+1]=="x"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][10]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][10]+1
                        elif (data[i][1][j+1]=="prt"):
                            self.TransmissionProbabilities[self.PartsofSpeechList[k]][11]=self.TransmissionProbabilities[self.PartsofSpeechList[k]][11]+1
        for i in range(0,12):
            self.TransmissionProbabilities["adj"][i]=(float(self.TransmissionProbabilities["adj"][i])/float(self.ADJcount))+0.00000000001
            self.TransmissionProbabilities["adv"][i]=(float(self.TransmissionProbabilities["adv"][i])/float(self.ADVcount))+0.00000000001
            self.TransmissionProbabilities["adp"][i]=(float(self.TransmissionProbabilities["adp"][i])/float(self.ADPcount))+0.00000000001
            self.TransmissionProbabilities["conj"][i]=(float(self.TransmissionProbabilities["conj"][i])/float(self.CONJcount))+0.00000000001
            self.TransmissionProbabilities["det"][i]=(float(self.TransmissionProbabilities["det"][i])/float(self.DETcount))+0.00000000001
            self.TransmissionProbabilities["noun"][i]=(float(self.TransmissionProbabilities["noun"][i])/float(self.nouncount))+0.00000000001
            self.TransmissionProbabilities["num"][i]=(float(self.TransmissionProbabilities["num"][i])/float(self.NUMcount))+0.00000000001
            self.TransmissionProbabilities["pron"][i]=(float(self.TransmissionProbabilities["pron"][i])/float(self.PRONcount))+0.00000000001
            self.TransmissionProbabilities["verb"][i]=(float(self.TransmissionProbabilities["x"][i])/float(self.VERBcount))+0.00000000001
            self.TransmissionProbabilities["x"][i]=(float(self.TransmissionProbabilities["adj"][i])/float(self.Xcount))+0.00000000001
            self.TransmissionProbabilities["."][i]=(float(self.TransmissionProbabilities["."][i])/float(self.Punctcount))+0.00000000001
            self.TransmissionProbabilities["prt"][i]=(float(self.TransmissionProbabilities["prt"][i])/float(self.PRTcount))+0.00000000001

        #Calculation of Emission probabilities of each word in the training corpus
        self.EmissionProbablities = defaultdict(lambda: [0,0,0,0,0,0,0,0,0,0,0,0],self.EmissionProbablities)
        for j in range(0, len(data)):
            for k in range(0,len(data[j][1])):
                if data[j][1][k]=="verb":
                    self.EmissionProbablities[data[j][0][k]][0]=self.EmissionProbablities[data[j][0][k]][0]+1
                elif data[j][1][k]=="noun":
                    self.EmissionProbablities[data[j][0][k]][1]=self.EmissionProbablities[data[j][0][k]][1]+1
                elif data[j][1][k]=="det":
                    self.EmissionProbablities[data[j][0][k]][2]=self.EmissionProbablities[data[j][0][k]][2]+1
                elif data[j][1][k]=="adj":
                    self.EmissionProbablities[data[j][0][k]][3]=self.EmissionProbablities[data[j][0][k]][3]+1
                elif data[j][1][k]=="pron":
                    self.EmissionProbablities[data[j][0][k]][4]=self.EmissionProbablities[data[j][0][k]][4]+1
                elif data[j][1][k]=="conj":
                    self.EmissionProbablities[data[j][0][k]][5]=self.EmissionProbablities[data[j][0][k]][5]+1
                elif data[j][1][k]=="adv":
                    self.EmissionProbablities[data[j][0][k]][6]=self.EmissionProbablities[data[j][0][k]][6]+1
                elif data[j][1][k] == ".":
                    self.EmissionProbablities[data[j][0][k]][7]=self.EmissionProbablities[data[j][0][k]][7]+1
                elif data[j][1][k]=="adp":
                    self.EmissionProbablities[data[j][0][k]][8]=self.EmissionProbablities[data[j][0][k]][8]+1
                elif data[j][1][k]=="num":
                    self.EmissionProbablities[data[j][0][k]][9]=self.EmissionProbablities[data[j][0][k]][9]+1
                elif data[j][1][k]=="x":
                    self.EmissionProbablities[data[j][0][k]][10]=self.EmissionProbablities[data[j][0][k]][10]+1
                elif data[j][1][k]=="prt":
                    self.EmissionProbablities[data[j][0][k]][11]=self.EmissionProbablities[data[j][0][k]][11]+1


        for key in self.EmissionProbablities:
            WordOccurenceNum=sum(self.EmissionProbablities[key])
            if WordOccurenceNum==0:
                WordOccurenceNum=1
            for i in range(0,12):
                self.EmissionProbablities[key][i]=(float(self.EmissionProbablities[key][i])/float(WordOccurenceNum))+0.00000000001
        pass
    #return final tags list for output based on the indices.
    def getFinalSequence(self, FinalIndexes):
        ListFinal=[]
        for i in range(0, len(FinalIndexes)):
            if FinalIndexes[i]==0:
                ListFinal.append('verb')
            elif FinalIndexes[i]==1:
                ListFinal.append('noun')
            elif FinalIndexes[i]==2:
                ListFinal.append('det')
            elif FinalIndexes[i]==3:
                ListFinal.append('adj')
            elif FinalIndexes[i]==4:
                ListFinal.append('pron')
            elif FinalIndexes[i]==5:
                ListFinal.append('conj')
            elif FinalIndexes[i]==6:
                ListFinal.append('adv')
            elif FinalIndexes[i]==7:
                ListFinal.append('.')
            elif FinalIndexes[i]==8:
                ListFinal.append('adp')
            elif FinalIndexes[i]==9:
                ListFinal.append('num')
            elif FinalIndexes[i]==10:
                ListFinal.append('x')
            elif FinalIndexes[i]==11:
                ListFinal.append('prt')
        return ListFinal


    #ADJ (adjective),ADV (adverb), ADP (adposition), CONJ (conjunction), DET (determiner), NOUN, NUM (number), PRON
    #(pronoun), PRT (particle), VERB, X (foreign word), and . (punctuation mark).
    # Functions for each algorithm.
    #
    def best(self, sentence):
        ListFinalindex=[]
        for i in range(0, len(sentence)):
            if sentence[i] in self.EmissionProbablities:
                ListFinalindex.append(self.EmissionProbablities[sentence[i]].index(max(self.EmissionProbablities[sentence[i]])))
            else:
                ListFinalindex.append(self.TransmissionProbabilities[sentence[i]].index(max(self.TransmissionProbabilities[ListFinalindex[i-1]])))
        ListFinalTags=self.getFinalSequence(ListFinalindex)
        return [[ListFinalTags], []]

    def mcmc(self, sentence, sample_count):
        wordPosteriorProbDict= {}
        wordPosteriorProbDict = defaultdict(lambda: [0,0,0,0,0,0,0,0,0,0,0,0],wordPosteriorProbDict)
        listfinal=[]
        SamplesList=[]
        SamplesListforMaxMarginal=[]
        initialSample=[ "noun" ] * len(sentence)
        SamplesList.append(initialSample[:])
        for n in range(0,20):
            for j in range(0,len(sentence)):
                for k in range(0,12):
                    if j==0:
                        if len(sentence)>1:
                            wordPosteriorProbDict[sentence[j]][k] = float(self.TransmissionProbabilities[self.PartsofSpeechList[k]][self.PartsofSpeechList.index(initialSample[j+1])])*float(self.EmissionProbablities[sentence[j]][k])

                    elif j==(len(sentence)-1):
                        if len(sentence)>1:
                            wordPosteriorProbDict[sentence[j]][k] = float(self.TransmissionProbabilities[initialSample[j-1]][k])*float(self.EmissionProbablities[sentence[j]][k])

                    else:
                        wordPosteriorProbDict[sentence[j]][k] = float(self.TransmissionProbabilities[initialSample[j-1]][k])*float(self.TransmissionProbabilities[self.PartsofSpeechList[k]][self.PartsofSpeechList.index(initialSample[j+1])])*float(self.EmissionProbablities[sentence[j]][k])
                initialSample[j] = self.PartsofSpeechList[wordPosteriorProbDict[sentence[j]].index(max(wordPosteriorProbDict[sentence[j]]))]
                SamplesListforMaxMarginal.append(initialSample[:])
                if initialSample not in SamplesList:
                    SamplesList.append(initialSample[:])
            initialSample[random.choice(list(range(0, len(sentence))))]=random.choice(self.PartsofSpeechList)

        for i in range(0, len(sentence)):
            for j in range(0,len(SamplesListforMaxMarginal)):
                if SamplesListforMaxMarginal[j][i]=="verb":
                    self.EmissionProbSample[sentence[i]][0]=self.EmissionProbSample[sentence[i]][0]+1
                elif SamplesListforMaxMarginal[j][i]=="noun":
                    self.EmissionProbSample[sentence[i]][1]=self.EmissionProbSample[sentence[i]][1]+1
                elif SamplesListforMaxMarginal[j][i] =="det":
                    self.EmissionProbSample[sentence[i]][2]=self.EmissionProbSample[sentence[i]][2]+1
                elif SamplesListforMaxMarginal[j][i] =="adj":
                    self.EmissionProbSample[sentence[i]][3]=self.EmissionProbSample[sentence[i]][3]+1
                elif SamplesListforMaxMarginal[j][i]=="pron":
                    self.EmissionProbSample[sentence[i]][4]=self.EmissionProbSample[sentence[i]][4]+1
                elif SamplesListforMaxMarginal[j][i]=="conj":
                    self.EmissionProbSample[sentence[i]][5]=self.EmissionProbSample[sentence[i]][5]+1
                elif SamplesListforMaxMarginal[j][i]=="adv":
                    self.EmissionProbSample[sentence[i]][6]=self.EmissionProbSample[sentence[i]][6]+1
                elif SamplesListforMaxMarginal[j][i] == ".":
                    self.EmissionProbSample[sentence[i]][7]=self.EmissionProbSample[sentence[i]][7]+1
                elif SamplesListforMaxMarginal[j][i]=="adp":
                    self.EmissionProbSample[sentence[i]][8]=self.EmissionProbSample[sentence[i]][8]+1
                elif SamplesListforMaxMarginal[j][i]=="num":
                    self.EmissionProbSample[sentence[i]][9]=self.EmissionProbSample[sentence[i]][9]+1
                elif SamplesListforMaxMarginal[j][i]=="x":
                    self.EmissionProbSample[sentence[i]][10]=self.EmissionProbSample[sentence[i]][10]+1
                elif SamplesListforMaxMarginal[j][i]=="prt":
                    self.EmissionProbSample[sentence[i]][11]=self.EmissionProbSample[sentence[i]][11]+1

        for key in self.EmissionProbSample:
            WordOccurenceNum=sum(self.EmissionProbSample[key])
            if WordOccurenceNum==0:
                WordOccurenceNum=1
            for i in range(0,12):
                self.EmissionProbSample[key][i]=float(self.EmissionProbSample[key][i])/float(WordOccurenceNum)

        if len(sentence)>1:
            if len(SamplesList)>30:
                for i in range(25,25+sample_count):
                    listfinal.append(SamplesList[i])
                return [ listfinal, [] ]
            elif len(SamplesList)<5:
                for i in range(0,len(SamplesList)):
                    listfinal.append(SamplesList[i])
                return [ listfinal, [] ]
            elif len(SamplesList)>5:
                listfinal= SamplesList[-5:]
                return [ listfinal, [] ]
            else:
                return [ [ [ "verb" ] * len(sentence) ] * sample_count, [] ]

        else:
            return [ [ [ "." ] * len(sentence) ] * sample_count, [] ]




    def naive(self, sentence):
        ListFinalindex=[]
        for i in range(0, len(sentence)):
            ListFinalindex.append(self.EmissionProbablities[sentence[i]].index(max(self.EmissionProbablities[sentence[i]])))
        ListFinalTags=self.getFinalSequence(ListFinalindex)


        return [[ListFinalTags], []]

    def max_marginal(self, sentence):

        ListFinalindex=[]
        ListFinalTags=[]
        ListFinalEmissionProbabilities=[]
        for i in range(0, len(sentence)):
            ListFinalindex.append(self.EmissionProbSample[sentence[i]].index(max(self.EmissionProbSample[sentence[i]])))
            ListFinalEmissionProbabilities.append(round(max(self.EmissionProbSample[sentence[i]]),2))
        for i in range(0,len(sentence)):
            ListFinalTags.append(self.PartsofSpeechList[ListFinalindex[i]])

        return [ [ListFinalTags], [ListFinalEmissionProbabilities] ]

    def viterbi(self, sentence):
        ListViterbi=[]
        listEmissionProbabilities=[]
        for i in range(0,len(sentence)):
            for j in range(0,12):
                if i==0:
                    self.ViterbiSequence[sentence[i]][j] = float(self.EmissionProbablities[sentence[i]][j])*float(self.InitialProbabilitiesList[self.PartsofSpeechList[j]])
                else:
                    for k in range(0,12):
                        listEmissionProbabilities.append(self.ViterbiSequence[sentence[i-1]][k]*self.TransmissionProbabilities[self.PartsofSpeechList[j]][k])
                    self.ViterbiSequence[sentence[i]][j]= float(self.EmissionProbablities[sentence[i]][j])*max(listEmissionProbabilities)
                    del listEmissionProbabilities[:]
        for i in range(0, len(sentence)):
            if all(v == 0.0 for v in self.ViterbiSequence[sentence[i]]):
                maxLikelihoodIndex=self.EmissionProbablities[sentence[i]].index(max(self.EmissionProbablities[sentence[i]]))
            else:
                maxLikelihoodIndex= self.ViterbiSequence[sentence[i]].index(max(self.ViterbiSequence[sentence[i]]))
            if maxLikelihoodIndex==0:
                ListViterbi.append('verb')
            elif maxLikelihoodIndex==1:
                ListViterbi.append('noun')
            elif maxLikelihoodIndex==2:
                ListViterbi.append('det')
            elif maxLikelihoodIndex==3:
                ListViterbi.append('adj')
            elif maxLikelihoodIndex==4:
                ListViterbi.append('pron')
            elif maxLikelihoodIndex==5:
                ListViterbi.append('conj')
            elif maxLikelihoodIndex==6:
                ListViterbi.append('adv')
            elif maxLikelihoodIndex==7:
                ListViterbi.append('.')
            elif maxLikelihoodIndex==8:
                ListViterbi.append('adp')
            elif maxLikelihoodIndex==9:
                ListViterbi.append('num')
            elif maxLikelihoodIndex==10:
                ListViterbi.append('x')
            elif maxLikelihoodIndex==11:
                ListViterbi.append('prt')

        return [[ListViterbi], []]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

