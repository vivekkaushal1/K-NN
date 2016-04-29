import csv
import random
import math
import operator
import numpy as np
import scipy
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsClassifier
 
def LoadDataset(filename, splitRatio, TrainingData=[] , TestData=[]):
        with open(filename, 'r') as csvfile:
            rows = csv.reader(csvfile)
            DataSet = list(rows)
            for x in range(len(DataSet)-1):
                for y in range(4):
                    DataSet[x][y] = float(DataSet[x][y])
                if random.random() < splitRatio:
                    TrainingData.append(DataSet[x])
                else:
                    TestData.append(DataSet[x])
            
                        
def EuclideanDis(Xvalue, Yvalue, length):
        distance = 0
        for x in range(int(length)):
                distance += float(pow((int(Xvalue[x]) - int(Yvalue[x])), 2))
        return math.sqrt(distance)
 
def GetNeighbors(TrainingData, TestingInstance, k):
        distances = []
        length = len(TestingInstance)-1
        for x in range(len(TrainingData)):
                dist = (float(EuclideanDis(TestingInstance, TrainingData[x], int(length))))
                distances.append((TrainingData[x], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
                neighbors.append(distances[x][0])
        return neighbors
 
def GetResponse(neighbors):
        ClassVotes = {}
        for x in range(len(neighbors)):
                response = neighbors[x][-1]
                if response in ClassVotes:
                        ClassVotes[response] += 1
                else:
                        ClassVotes[response] = 1
        SortedVotes = sorted(ClassVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
        return SortedVotes[0][0]
 
def GetAccuracy(TestData, predictions):
        correct = 0
        for x in range(len(TestData)):
                if TestData[x][-1] == predictions[x]:
                        correct += 1
        return (correct/float(len(TestData))) * 100.0


                    
def main():

        k = input('Give the value of K : ')
        outputFile = open('outputTrans.txt','a')
        TrainingData=[]
        TestData=[]
        
        splitRatio = 0.70
       
        LoadDataset('transfusion.csv', splitRatio, TrainingData, TestData)
        print '===Splitting the data===='
        print 'Train set:'+str(len(TrainingData))
        print 'Test set:'+str(len(TestData))
        print 'Writing the predictions and actual values to the file..'
        
        predictions=[]
        
        for x in range(len(TestData)):
                neighbors =(GetNeighbors(TrainingData, TestData[x], int(k)))
                result = GetResponse(neighbors)
                predictions.append(result)
                conOutput = ('> predicted=' + repr(result) + ', actual=' + repr(TestData[x][-1]) + '\n')
                outputFile.write(conOutput)
        accuracy = GetAccuracy(TestData, predictions)
        accu = ('Accuracy: ' + repr(accuracy) + '%')
        outputFile.write(accu)
        
        print 'File with the output values generated..'
        
        
main()
