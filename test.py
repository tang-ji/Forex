from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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

alldata = ClassificationDataSet(3, 1, nb_classes=3)
datingDataMat, datingLabels = file2matrix('E:\Documents\Python\kNN\datingTestSet.txt')
normMat, ranges, minValues = autoNorm(datingDataMat)
for i in range(len(normMat)):
    alldata.addSample(normMat[i], (datingLabels[i] - 1) / 2)

tstdata, trndata = alldata.splitWithProportion(0.25)
trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]
fnn = buildNetwork(trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.01, verbose=True, weightdecay=0.0001)
ticks = arange(-1., 1., 0.1)
X, Y, Z = meshgrid(ticks, ticks, ticks)
# need column vectors in dataset, not arrays
griddata = ClassificationDataSet(3, 1, nb_classes=3)
for i in xrange(X.size):
    griddata.addSample([X.ravel()[i], Y.ravel()[i], Z.ravel()[i]], [0])
griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy
for i in range(20):
    trainer.trainEpochs(1)
    trnresult = percentError(trainer.testOnClassData(), trndata['class'])
    tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
    print "epoch: %4d" % trainer.totalepochs, "train error: %5.2f%%" % trnresult, "test error: %5.2f%%" % tstresult
    out = fnn.activateOnDataset(griddata)
    out = out.argmax(axis=1)  # the highest output activation gives the class
    out = out.reshape(X.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    hold(True)    # overplot on
    for c in [0, 1, 2]:
        here, _ = where(tstdata['class'] == c)
        ax.plot_trisurf(tstdata['input'][here, 0], tstdata['input'][here, 1], tstdata['input'][here, 2])
    if out.max() != out.min():  # safety check against flat field
        contourf(X, Y, Z, out)   # plot the contour
    plt.show()
