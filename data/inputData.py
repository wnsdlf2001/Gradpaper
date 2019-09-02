'''
Created on Sep 19, 2012

@author: ego
'''
import numpy as np
from sklearn.preprocessing import normalize

class inputData(object):
    '''
        Here we deal with the generation of input words and their decomposition
        in subwords ...
    '''

    def __init__(self):
        self.data = []

    
    def addOne(self,inputValue):
       # if not isinstance(inputValue,np.ndarray):
        #    raise(ValueError,'Input should belong to np.ndarray')
#        if not isinstance(outputValue,np.ndarray):
#            raise(ValueError,'Output should belong to np.ndaray')
        self.data.append((inputValue))
        
    def addAll(self, allData):
        for inputs in allData:
            self.addOne(inputs)
        return self.data
        
    def getData(self,index):
        if index > len(self.data):
            raise(ValueError,'Index exceeds list''s length')
        return self.data[index]
    
    def getSubWords(self, index, subwordlist):
        '''
        Return the subwords decomposition of the pattern with the specified index
        The subwords are normalized [0...1] by dividing the array to the max value in the array
        '''
        subwords = []
        prev=0
        for num in range(len(subwordlist)):
            result = 0
            if num ==0:
                tmp = np.array(self.data[index][0][result:result + subwordlist[num]], dtype='f8')
                prev = result + subwordlist[num]
            else:
                for i in range(num+1):
                    result += subwordlist[i]
                tmp = np.array(self.data[index][0][prev:result], dtype='f8')
                prev = result
            subwords.append(tmp)
        return subwords
    
    def getWholeArray(self, index):
        return self.data[index][0]
    
    def getSubWordsWithNoise(self, index):
        noisePercent = 0.2
        subwords = []
        for i in range(self.data[0][0].shape[0]):
            tmp = self.normalize(self.data[index][0][i,:])
            subwords.append(tmp)
        for i in range(int(len(subwords)*noisePercent/2)):
            idx1 = np.random.randint(self.data[0][0].shape[1])
            idx2 = np.random.randint(self.data[0][0].shape[1])
            subwords[idx1],subwords[idx2] = subwords[idx2],subwords[idx1]

        for i in range(self.data[0][0].shape[1]):
            tmp = self.normalize(self.data[index][0][:,i])
            subwords.append(tmp)
        for i in range(int(len(subwords)*noisePercent/2)):
            idx1 = np.random.randint(self.data[0][0].shape[0])
            idx2 = np.random.randint(self.data[0][0].shape[0])
            subwords[idx1],subwords[idx2] = subwords[idx2],subwords[idx1]
        
        return subwords
        
    def getOutputs(self,index):
        return self.data[index][1]
    
    def getCount(self):
        return len(self.data)

    def normalize(self, subword):
       # normedsubword = normalize(subword, axis = 1, norm='l2')
       # normedsubword =[]
       # for i in subword:
       #     normedsubword.append(float(i)/float(max(subword)))
        checkzero = 0
        for i in range(len(subword)):
            if subword[i] == 0:
                checkzero+=1
        if checkzero == len(subword):
            return subword
        else:
            normedsubword = subword / subword.max()
            return normedsubword # [0] 추가?
        