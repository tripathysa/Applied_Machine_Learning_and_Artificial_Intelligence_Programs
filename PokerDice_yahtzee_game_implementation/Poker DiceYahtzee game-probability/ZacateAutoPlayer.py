# Automatic Zacate game player
# B551 Fall 2015
# Name: Saurabh Tripathy , USERID: saurtrip
#
# Based on skeleton code by D. Crandall
#
# The game is tested to play 100 games multiple times and
# avg. score lies between 180 to 190 each time.
# max score ranging between 260 to 330 each time.
# Strategy: The algorithm uses somewhat greedy approach to obtain maximum scores.
#First strategy is always to check if we can get bonus of 35 points if we get 63 points bonus amongst first 6 categories.
#For that, we assign first 6 outcomes first in order than later 7 categories,only if number of each tern repeats at least 3 times which will reach closer to 63
#Then we target the categories quintupulo,pupusa de queso, pupusa de frijol, "elote", "cuadruple", "triple", "tamal" in that order.
#Reroll logic:
#Reroll logic again follows a greedy approach in which if get a favourable outcome, we keep that outcome safe and reroll the other dice.
# e.g Like if we get a 1,2,3,4 we find the 5th dice and reroll it to get pupusa de queso
# if we get 3 numbers same, then reroll other two if they are not same to target quintupulo or cuadruple or elote.
# Same way if we get 4 numbers same, then reroll other one to target quintupulo  or elote.



# This is the file you should modify to create your new smart Zacate player.
# The main program calls this program three times for each turn. 
#   1. First it calls first_roll, passing in a Dice object which records the
#      result of the first roll (state of 5 dice) and current Scorecard.
#      You should implement this method so that it returns a (0-based) list 
#      of dice indices that should be re-rolled.
#   
#   2. It then re-rolls the specified dice, and calls second_roll, with
#      the new state of the dice and scorecard. This method should also return
#      a list of dice indices that should be re-rolled.
#
#   3. Finally it calls third_roll, with the final state of the dice.
#      This function should return the name of a scorecard category that 
#      this roll should be recorded under. The names of the scorecard entries
#      are given in Scorecard.Categories.
#
import collections
from collections import Counter
from ZacateState import Dice
from ZacateState import Scorecard
import random

class ZacateAutoPlayer:
      def __init__(self):
            pass  

      def first_roll(self, dice, scorecard):
          counts = [dice.dice.count(i) for i in range(1,7)]
          listFinal=[]
          if ((not scorecard.scorecard.has_key('pupusa de queso')) and (sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6])):
              return []
          elif (len(set([1,2,3,4]) - set(dice.dice)) == 0):
              return [dice.dice.index(list((Counter(dice.dice) - Counter([1,2,3,4])).elements())[0])]
          elif (len(set([2,3,4,5]) - set(dice.dice)) == 0):
              return [dice.dice.index(list((Counter(dice.dice) - Counter([2,3,4,5])).elements())[0])]
          elif (len(set([3,4,5,6]) - set(dice.dice)) == 0):
              return []
          elif (not scorecard.scorecard.has_key('elote')) and (2 in counts) and (3 in counts):
              return []
          elif (not scorecard.scorecard.has_key('quintupulo')) and (max(counts) == 5):
              return []
          elif ((3 in counts) and (1 in counts)) or ((3 in counts) and (2 in counts)):
              for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(3)+1:
                      listFinal.append(i)
              return listFinal
          elif (4 in counts) and (1 in counts):
              for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(4)+1:
                      return [i]
          elif (2 in counts) and (3 not in counts) and (4 not in counts) and (5 not in counts):
              del listFinal[:]
              for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(2)+1:
                      listFinal.append(i)
              return listFinal
          else:
              return [0,1,2,3,4]

      def second_roll(self, dice, scorecard):
          counts = [dice.dice.count(i) for i in range(1,7)]
          listFinal=[]
          if ((not scorecard.scorecard.has_key('pupusa de queso')) and (sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6])):
              return []
          elif (len(set([1,2,3,4]) - set(dice.dice)) == 0):
            return [dice.dice.index(list((Counter(dice.dice) - Counter([1,2,3,4])).elements())[0])]
          elif (len(set([2,3,4,5]) - set(dice.dice)) == 0):
            return [dice.dice.index(list((Counter(dice.dice) - Counter([2,3,4,5])).elements())[0])]
          elif (len(set([3,4,5,6]) - set(dice.dice)) == 0):
            return []
          elif (not scorecard.scorecard.has_key('elote')) and (2 in counts) and (3 in counts):
            return []
          elif (not scorecard.scorecard.has_key('quintupulo')) and (max(counts) == 5):
            return []
          elif ((3 in counts) and (1 in counts)) or ((3 in counts) and (2 in counts)):
            for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(3)+1:
                      listFinal.append(i)
            return listFinal
          elif (4 in counts) and (1 in counts):
            for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(4)+1:
                      return [i]
          elif (2 in counts) and (3 not in counts) and (4 not in counts) and (5 not in counts):
            del listFinal[:]
            for i, item in enumerate(dice.dice):
                  if item >0 and item != counts.index(2)+1:
                      listFinal.append(i)
            return listFinal
          else:
            return [0,1,2,3,4]
      
      def third_roll(self, dice, scorecard):
          listFinal=[]
          Ctgry = [ "unos", "doses", "treses", "cuatros", "cincos", "seises", "pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo", "tamal" ]
          counts = [dice.dice.count(i) for i in range(1,7)]
          if (5 in counts) and not scorecard.scorecard.has_key('quintupulo'):
              return 'quintupulo'
          elif ((not scorecard.scorecard.has_key('pupusa de queso')) and ((sorted(dice.dice) == [1,2,3,4,5]) or (sorted(dice.dice) == [2,3,4,5,6]))):
              return 'pupusa de queso'
          elif ((len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) and not scorecard.scorecard.has_key('pupusa de frijol')):
              return 'pupusa de frijol'
          elif ((counts[5]>2) and (not scorecard.scorecard.has_key('seises'))):
              return 'seises'
          elif ((counts[4]>2) and (not scorecard.scorecard.has_key('cincos'))):
              return 'cincos'
          elif ((counts[3]>2) and (not scorecard.scorecard.has_key('cuatros'))):
              return 'cuatros'
          elif ((counts[2]>2) and (not scorecard.scorecard.has_key('treses'))):
              return 'treses'
          elif ((counts[1]>2) and (not scorecard.scorecard.has_key('doses'))):
              return 'doses'
          elif ((counts[0]>2) and (not scorecard.scorecard.has_key('unos'))):
              return 'unos'
          elif (2 in counts) and (3 in counts) and (not scorecard.scorecard.has_key('elote')):
              return 'elote'
          elif max(counts) >= 4 and (not scorecard.scorecard.has_key('cuadruple')):
              return 'cuadruple'
          elif max(counts) >= 3 and (not scorecard.scorecard.has_key('triple')):
              return 'triple'
          elif ((counts[5]>0) and (not scorecard.scorecard.has_key('seises'))):
              return 'seises'
          elif ((counts[4]>0) and (not scorecard.scorecard.has_key('cincos'))):
              return 'cincos'
          elif ((counts[3]>0) and (not scorecard.scorecard.has_key('cuatros'))):
              return 'cuatros'
          elif ((counts[2]>0) and (not scorecard.scorecard.has_key('treses'))):
              return 'treses'
          elif ((counts[1]>0) and (not scorecard.scorecard.has_key('doses'))):
              return 'doses'
          elif ((counts[0]>0) and (not scorecard.scorecard.has_key('unos'))):
              return 'unos'
          elif (not scorecard.scorecard.has_key('tamal')):
              return 'tamal'
          else:
              if scorecard.scorecard:
                  listFinal=list(set(Ctgry)-set(scorecard.scorecard))
                  if listFinal:
                      return listFinal[0]



