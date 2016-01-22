#!/usr/bin/env python
#coding:utf-8
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from Tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#----------------------------------------------------------------------
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
      classLabelVector.append(float(listFromLine[-1])) #Get the evaluate of each person
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

def drawPic():
    try:
        sampleCount = int(inputEntry.get())
    except:
        sampleCount = 50
        print 'Enter an integer.'
        inputEntry.delete(0, END)
        inputEntry.insert(0, '50')
    # Need column vectors in dataset, not arrays
    for i in range(sampleCount):
        trainer.trainEpochs(1)
        trnresult = percentError(trainer.testOnClassData(), trndata['class'])
        tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
        if i % 20 == 0:
            t.delete(1.0, END)
        t.insert(END, "epoch:" + str(trainer.totalepochs) + "  train error:" + str(round(trnresult, 2)) \
                  + "%  test error:" + str(round(tstresult, 2)) + "%\n")
        # Clear the Figure
        drawPic.a = drawPic.f.add_subplot(111, projection='3d')
        drawPic.a.set_title('Training...')
        for a, c, m in [(0, 'r', 'o'), (1, 'b', '^'), (2, 'y', 's')]:
            out = fnn.activateOnDataset(alldata)
            out = out.argmax(axis=1)
            here = (out == a)
            drawPic.a.scatter(alldata['input'][here, 0], alldata['input'][here, 1], alldata['input'][here, 2], c=c, marker=m)
        drawPic.canvas.show()

if __name__ == '__main__':
    matplotlib.use('TkAgg')
    root = Tk()
    root.title('Neural network training')
    new = Tk()
    new.title('Note the errors')
    new.geometry('350x800')
    t = Text(new)
    t.grid(row=1, column=1, rowspan=50, columnspan=50)
    t.pack()
    # Putting a figure on GUI
    drawPic.f = Figure(figsize=(10, 7), dpi=108, facecolor="white")
    ax = drawPic.f.add_subplot(111, projection='3d')
    drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
    drawPic.canvas.show()
    drawPic.canvas.get_tk_widget().grid(row=0, columnspan=3)
    # Setting Labels and Text
    Label(root, text='Training times：').grid(row=1, column=0)
    inputEntry = Entry(root)
    inputEntry.grid(row=1, column=1)
    inputEntry.insert(0, '50')
    Button(root, text='Begin', command=drawPic).grid(row=1, column=2, columnspan=3)

    alldata = ClassificationDataSet(3, 1, nb_classes=3)
    datingDataMat, datingLabels = file2matrix('E:\Documents\Python\kNN\datingTestSet.txt')
    normMat, ranges, minValues = autoNorm(datingDataMat)
    for i in range(len(normMat)):
        alldata.addSample(normMat[i], [datingLabels[i] - 1])
    tstdata, trndata = alldata.splitWithProportion(0.25)
    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )
    alldata._convertToOneOfMany( )
    t.insert(END, "Number of training patterns: " + str(len(trndata)) + "\n")
    t.insert(END, "Input and output dimensions: " + str(trndata.indim) + str(trndata.outdim) + "\n")
    fnn = buildNetwork(trndata.indim, 100, 5, trndata.outdim, outclass=SoftmaxLayer)
    fnn.activate([3, 100, 1])
    trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.01, verbose=True, weightdecay=0.0001)
    # Begin the loop
    root.mainloop()