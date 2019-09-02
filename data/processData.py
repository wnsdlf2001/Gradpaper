'''
Created on Sep 21, 2012

@author: ego
'''
import numpy as np

class processData(object):
    '''
    processData reads the contents of a .pat file with the stored data set and:
     - brakes it in input/output pairs
     
     Eventually it should be merged with inputData and injectData
    '''


    def __init__(self, data, label):
        '''
        The __init__ takes as parameter the .pat file where the dataset is stored
        '''
        self.debug = 1
        self.data = data
        self.inputs = []
        self.outputs= []
        self.label = label

    def writeContents(self):
        line = self.f.readline()

    def readContents(self):
        inputData = []
        outputData = []
        for i in range(len(self.data)):
           outputData = self.data[i][self.label]
           inputData = self.data[i]
           self.outputs.append(outputData)
           self.inputs.append(inputData)

        self.result = zip(self.inputs, self.outputs)

        return self.result


if __name__ == '__main__':
            
    data = processData("data.pat")
    data.readContents()
        