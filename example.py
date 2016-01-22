from numpy import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import numpy as np

def file2matrix(filename):
   fr = open(filename) #Load the data
   NumbersOfLines = len(fr.readlines()) #Get the number of the lines
   returnMatrix = zeros((NumbersOfLines, 3)) #Create Numpy matrix to return
   classLabelVector = []
   fr = open(filename) #Reload the data
   index = 0
   for line in fr.readlines():
      lines = line.strip() #Strip the beginning and the end blank
      listFromLine = lines.split() #Separate each line by '\t'
      returnMatrix[index, :] = listFromLine[0:3] #Get the 3 values of each line
      classLabelVector.append(int(listFromLine[-1])) #Get the evaluate of each person
      index += 1
   return returnMatrix, classLabelVector
def autoNorm(dataSet):
   minValues = dataSet.min(0) #The min value
   maxValues = dataSet.max(0) #The max value
   ranges = maxValues - minValues
   # normDataset = zeros(shape(dataSet))
   m = dataSet.shape[0] #The number of lines
   normDataset = dataSet - tile(minValues, (m, 1))
   normDataset = normDataset/tile(ranges, (m, 1)) #Calculate the values normalized
   return normDataset, ranges, minValues
net = buildNetwork(3, 200, 100, 5, 1)
net.activate([3, 200, 1])
ds = SupervisedDataSet(3, 1)
datingDataMat, datingLabels = file2matrix('E:\Documents\Python\kNN\datingTestSet.txt')
normMat, ranges, minValues = autoNorm(datingDataMat)
for i in range(len(normMat)):
    ds.addSample(normMat[i], (datingLabels[i] - 1) / 2)
trainer = BackpropTrainer(net, ds, momentum=0.01, verbose=True, weightdecay=0.00001)
trainer.trainUntilConvergence()
# trainer.trainEpochs(epochs=500)
out = SupervisedDataSet(3, 1)
for i in range(len(normMat)):
    out.addSample(normMat[i], (datingLabels[i] - 1) / 2)
out = net.activateOnDataset(out)
print np.array(out)[:, 1]*2 + 1
