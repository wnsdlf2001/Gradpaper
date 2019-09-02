'''
Created on Sep 25, 2012

@author: ego
'''
from datetime import date
import re
import os
import data.processData
import numpy as np
import pandas as pd



class injectData(object):
    '''
    This class injects patterns into a .pat file. The constructor takes the filename 
    as a paramter.The file if exists is overwritten
    '''

    def __init__(self, filename, directory, mode):
        '''
        Constructor
        '''
        self.directory = directory
        self.filename = filename
        self.index = 1
        self.mode = mode

    def injectData(self):
        data = []
        traindata = []
        testdata = []
        f = open(self.filename)
        for line in f:
            inner_list = []
            inner_list += ([elt.strip() for elt in line.split(',')])
            data.append(inner_list)
        f.close()
        for i in range(len(data[0])):
            tmp =[]
            for j in range(len(data)):
                tmp.append(data[j][i])
            tmp = list(map(float, tmp))
            tmp = self.normalize(tmp)
            for k in range(len(data)):
                data[k][i] = tmp[k]


        if self.mode == 'train':
            traindata = data
            return traindata
        elif self.mode == 'test':
            testdata = data
            return testdata

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
            newList = [float(x) / float(max(subword)) for x in subword]
            return newList

if __name__ == '__main__':
   data = injectData('test/switzdataset2.txt', 'data/test', 'test')
