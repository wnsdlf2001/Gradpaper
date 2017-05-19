#!/usr/bin/env python

'''
Created on Nov 12, 2012

@author: ego
'''
from data.injectData import injectData
from data.processData import processData
from data.inputData import inputData
import Lamstar
import os




class runConsole(object):
    def __init__(self):
        self.trainingDir = 'data/'
        self.trainPat = self.trainingDir + 'clevedataset2.txt'
        self.trainPat2 = self.trainingDir + 'data.pat'
        self.testingDir = 'data/test/'
        self.testPat = self.testingDir+'switzdataset2.txt'
        self.testPat2 = self.testingDir + 'test.pat'
        self.debug = 1
        self.prepareTraining()
        self.prepareTesting()
        self.train('train')
        self.train('test')


    def prepareTraining(self):
        if self.trainingDir is None:
            return None
        self.log('Cleaning previous temporary data ...','main')
        #self.cleanDir(self.trainingDir)
        self.log('Starting training operations ...', 'main')
        directory = self.trainingDir
        outdir = directory + '/'
        self.log('Getting data ...', 'query')
        self.log('Saving patterns in the .pat file ...', 'query')
        trainpat = injectData(self.trainPat, outdir, 'train')
        self.log('OK', 'status')

    def prepareTesting(self):
        if self.testingDir is None:
            return None
        self.log('Cleaning previous temporary data ...', 'main')
        #self.cleanDir(self.testingDir)
        self.log('Starting testing operations ...', 'main')
        directory = self.testingDir
        outdir = directory + '/'
        #self.log('Getting faces ...', 'query')
        #fd = faceDetector(outdir,outdir)
        #fd.run()
        #self.log('OK', 'status')
        self.log('Saving patterns in the .pat file ...', 'query')
        injectData(self.testPat, outdir, 'test')
        self.log('OK', 'status')

    def train(self, bywho):
        #allSamples = goodSamples = 0.0
        self.log('Starting the real training...', 'main')
        if bywho == 'train':
            procData = processData(self.trainPat2)
            result = procData.readContents()
            data = inputData()
            data.addAll(result)
            self.ls = Lamstar.lamstar(15, 1)
            for iter in range(10):#num of training
                print('Iteration %s' % iter)
                for i in range(14): #num of subwords
                    print('Training data : ', i)
                    self.ls.train(data.getSubWords(i), data.getOutputs(i))
                if(self.debug > 0):
                    self.log('Iteration no:' + str(iter), 'main')
                    self.log('No of nodes' + str(self.ls.getNoOfNodes()), 'main')

        elif bywho == 'test':
            procData = processData(self.testPat2)
            result = procData.readContents()
            data = inputData()
            data.addAll(result)
            files = []
            print('Quering for test data')
            self.log('Quering for test data', 'main')
            print('number of items: %s' % (data.getCount()))
            for i in range(data.getCount()):
                #self.log('Querying for ' + files[i].rpartition('/')[-1], 'query')
                #print('Querying for ' + files[i].rpartition('/')[-1])
                (result, BMU) = self.ls.query(data.getSubWords(i))
                self.log(result, 'status')
                #allSamples += 1
                #if files[i].find(result) != -1:
                    #goodSamples += 1
            self.log('No of nodes: ' + str(self.ls.getNoOfNodes()), 'main')
            self.log('No of links: ' + str(self.ls.getNoOfLinks()), 'main')
            #self.log('Accuracy = ' + str((float(goodSamples) / allSamples) * 100) + '%', 'main')

    def cleanDir(self, inputDir):
        for afile in os.listdir(inputDir):
            if afile.find('procced') != -1:
                os.remove(inputDir + '/' + afile)

    def log(self, text, mode):
        if(mode == 'query'):
            print(text)
        elif(mode == 'main'):
            print(text)
if __name__ == '__main__':
    runConsole()
