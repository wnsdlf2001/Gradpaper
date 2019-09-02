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
import random

class runConsole(object):
    def __init__(self):
        self.trainingDir = 'data/'
        self.trainingData = self.trainingDir + 'brain.txt' #'Traumatic.txt' 'Heartdisease.txt' 'Breastcancer.txt'
        self.debug = 11
        self.label = 41 # output value 가 있는 index (0부터 시작)
        self.iternum = 2 # lamstar training iteration number
        self.distanceThreshold = 0.01# Threshold for BMU distance
        self.subwordlist = [1,1,1,1,1,1,1,1,2,1,1,1,7,1,4,1,6,4,5]
        self.subwordnumber = 13
        self.trainnumber = 100
        self.testnumber = 50


        data = self.prepareTraining()
        self.log('Starting the training...', 'main')
        for i in range(20):
            self.train(data, self.iternum, self.distanceThreshold, 'train')
            self.train(data, self.iternum, self.distanceThreshold, 'test')
            self.iternum += 1

    def prepareTraining(self):
        if self.trainingDir is None:
            return None
        self.log('Preparing Datasets..', 'main')
        directory = self.trainingDir
        print("#Size of dataset: " + str(self.trainnumber),"@Input file name: " + self.trainingData[5:-4],
              "%Threshold:" + str(self.distanceThreshold))
        outdir = directory + '/'
        traindata = injectData(self.trainingData, outdir, 'train').injectData()
        return traindata

    def train(self, traindata, iternum, distth, bywho,):

        procData = processData(traindata, self.label)
        result = procData.readContents()
        data = inputData()
        data.addAll(result)
        b = []
        for i in range(0, data.getCount()):
            b.append(i)
        if bywho == 'train':
            if self.trainnumber > data.getCount():#에외처리
                print("training data is larger than number of dataset. Choose trainnum lower than " + str(
                    data.getCount()))
                return 0
            self.ls = Lamstar.lamstar(self.subwordnumber, 1)  #램스타 객체 생성(서브워드 갯수만큼)
            #b = random.sample(range(0, data.getCount()), self.trainnumber)
            for iter in range(iternum):
                #print('Training Iteration %s' % iter)
                for i in range(self.trainnumber): #num of subwords
                    #print('Training data : ', b[i])  #샘플링 데이터 인덱스 확인 가능
                    self.ls.train(data.getSubWords(b[i], self.subwordlist), data.getOutputs(b[i]), distth)#트레이닝


        elif bywho =='test':
            b = b[data.getCount()-self.testnumber:data.getCount()]
            accuarcy = 0
            TP = 0
            TN = 0
            FP = 0
            FN = 0
            #if self.testnumber > data.getCount():
            #    print("testing data is larger than number of dataset. Choose testnum lower than " + str(data.getCount()))
            #    return 0
            print("Training iteration: " + str(self.iternum))
            #a =[]
            #for i in range(0, data.getCount()):
            #    a.append(i)
            for i in range(len(b)):
            #    p = a[random.randrange(0, len(a) - 1)]

                #print("")
                #print("Validation "+str(i))
                queryvalue = self.ls.query(data.getSubWords(b[i], self.subwordlist))
                if queryvalue == data.getOutputs(b[i]):
               #     print("GT : " + data.getOutputs(i) +"  ST : " + queryvalue + " Result : TRUE")
                    accuarcy += 1
               # else:
               #     print("GT : " + data.getOutputs(i) + "  ST : " + queryvalue + " Result : FALSE")
               # print("")
                if int(data.getOutputs(b[i])) == 0 and int(queryvalue) == 0:
                    TN += 1
                if int(data.getOutputs(b[i])) == 1 and int(queryvalue) == 1:
                    TP += 1
                if int(data.getOutputs(b[i])) == 0 and int(queryvalue) == 1:
                    FP += 1
                if int(data.getOutputs(b[i])) == 1 and int(queryvalue) == 0:
                    FN += 1

            accuarcy /= int(len(b)) # 분할 validation 버젼
            #accuarcy /= self.testnumber #랜덤 샘플링 버젼
            #print("Accuarcy : " + str(accuarcy * 100) + "%")
            if TP ==20 : exit
            else:
                if TP + FP == 0:
                    prec = 0
                elif TN+FP ==0:
                    print("TN + FP is Zero! setting prec to 0")
                    prec = 0
                else:
                    prec = TN / (TN + FP)
                if TP + FN == 0:
                    rec = 0
                else:
                    rec = TP / (TP + FN)
            #accuracy = (TP + TN)/(TP + TN + FP + FN)
            #if (rec == 0) and (prec == 0): exit

                print("Sensitivity:"+ str(rec * 100)+ "%", "Precision:"+ str(prec * 100)+ "%", "Accuarcy:"+ str(accuarcy * 100) + "%")
                print("TP:" + str(TP) + "  TN:" + str(TN) + "  FP:" + str(FP) + "  FN:" + str(FN))
                print("")

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
