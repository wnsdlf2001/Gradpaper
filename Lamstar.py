



from data.processData import processData
from SOM.somModule import somModule
from data.inputData import inputData
from collections import defaultdict
from numpy import array
import sys


class lamstar(object):
    '''
    classdocs
    '''
    def __init__(self, noOfInputs, noOfOutputs):
        '''
        Constructor
        '''
        self.CriticalLink =[]
        self.debug = 1
        self.noOfInputs = noOfInputs
        self.noOfOutputs = noOfOutputs
        self.inputSOMs = []
        self.inputSOM = []
        self.outputSOMs = []
        for _ in range(noOfInputs):
            self.inputSOMs.append(somModule(1))
        for _ in range(noOfOutputs):
            self.outputSOMs.append(somModule(1))

        self.Link2OutputDict = {}
        self.Link2LinkDict = {}

    def train(self, inputs, outputs, threshold):
        '''
        In BMU we store in form of list of tuples, the link between BMU
        in the respective SOM and the respective output
        So finally BMU is a triple (somModuleNumber,BMU,output)
        '''
        prevNode = None
        for i in range(self.noOfInputs):
            nextNode = self.inputSOMs[i].train(array(inputs[i]), threshold) # 노드를 생성하면서 트레이닝
            if i != 0:
                self.reward((i, prevNode, nextNode, outputs)) # 리워딩 작업 # (시작 모듈, 출발노드, 도착노드, 아웃풋) : 웨이트
            prevNode = nextNode
        self.forget() # 포겟팅 작업


    def reward(self, key):
        if key in self.Link2OutputDict.keys():
            self.Link2OutputDict[key] += 1
        else:
            self.Link2OutputDict[key] = 1

    def forget(self):
        for key in self.Link2OutputDict.keys():
            self.Link2OutputDict[key] *= 0.99

    def goToSleep(self):
        '''
        Here we perform tasks that compact and optimize the database ...
        The Algorithm goes to sleep for regeneration :)
        '''
        self.hashTable = {}
        for key in self.Link2OutputDict.keys():
            print(key, key[0])
            self.hashTable.setdefault(key[0], []).append(key)
        self.hashTable = self.Link2OutputDict
        return self.hashTable

    def query(self, inputs):
        '''
        Here BMU is just a list of tuples(2 values) that hold the pair
        (somModule,BMU(best somNode in somModule)).
        '''


        BMU = []
        PrevNode = None
        for i in range(self.noOfInputs):
            NextNode = self.inputSOMs[i].query(inputs[i], self.Link2OutputDict, i)
            if i !=0:
                BMU.append((i, PrevNode, NextNode))  # list(self.Link2OutputDict.keys())[i][2]))
            PrevNode = NextNode


        db1 = defaultdict(list)
        for ahash in BMU:
            for key in self.Link2OutputDict.keys():
                if key[0:3] == ahash:
                    db1[key[-1]].append((key[0:3] , self.Link2OutputDict[key]))

        w = [[] for row in range(len(db1))]
        idx = 0
        for x in db1:
            for i in range(len(db1[x])):
                w[idx].append(db1[x][i][1])
            idx +=1
        '''
        idx = 0
        resultset = [[] for row in range(len(db1))]
        for m in range(len(w)):
            for k in range(len(w[m])):
                for i in range(k, len(w[m])):
                    result = 0
                    for j in range(k, i+1):
                        result += w[m][j]
                        div = i+1
                    resultset[idx].append(result/div)
            idx +=1'''
        db = defaultdict(list)
        for ahash in BMU:
            for key in self.Link2OutputDict.keys():
                if key[0:3] == ahash:
                    db[key[-1]].append(self.Link2OutputDict[key])
       #             print('key=%s db[key[-1]=%s' % (key, db[key[-1]]))

        #for x in db:


        flag = 0
        '''
        for j in range(0,len(BMU)):
            if j == 0:
                print(" Node    Weight    ",end='')
                for i in db1:
                    print("to "+ str(int(i))+"          ", end='')
                print("")
            print(str(BMU[j][1]) + " -> "+str(BMU[j][2]) +" : ",end='')
            for i in db1:
                    print(str(db1[i][j][1])+"   ", end='')
            print("")


        print('Scores for each outputs  : ')
        for key in db.keys():
            print('"%s" = %s' % (int(key), str(sum(db[key]))))
        print("result is " + str(int(self.maxFromDict(db))))
        '''
       # return result
        return self.maxFromDict(db)#(self.maxFromDict(db), BMU)



    def printSOMs(self):
        for i in range(self.noOfInputs):
            self.inputSOMs[i].printNodes()

    def getInputNode(self, i, index):
        return self.inputSOMs[i].getNodeAt(index)

    def getNoOfNodes(self):
        noNodes = 0
        best = 0
        for i in range(self.noOfInputs):
            noNodes = self.inputSOMs[i].getNoOfNodes()
            if noNodes > best:
                best = noNodes
        return noNodes

    def getNoOfLinks(self):
        return len(self.Link2OutputDict)

    def printTable(self):
        for key in self.LinkTable.keys():
            print('%s %s' % (key, self.LinkTable[key]))

    def maxFromDict(self, dictionary):
        #return min(dictionary.items(), key=lambda item: sum(item[1])/float(len(item[1])))[0]
        return max(dictionary.items(), key=lambda item: sum(item[1]))[0]


if __name__ == '__main__':

    #procData = processData('data/images/processed/all/150x200.pat')
    procData = processData('data/clevepro.pat')
    result = procData.readContents()
    data = inputData()
    data.addAll(result)

    # #preData = processData('data/images/processed/unseen/unseen.pat')
    # preData = processData('data/.txt')
    # result = preData.readContents()
    # unseenData = inputData()
    # unseenData.addAll(result)

    ls = lamstar(10, 1)
    for _ in range(10):
        for i in range(data.getCount()):
           print('Training data : ', i)
           ls.train(data.getSubWords(i), data.getOutputs(i))
    #sys.stdin.read(1)

    ls.printSOMs()
    #ls.printTable()

    print('\nQuering without noise:')
    for i in range(data.getCount()):
        print('\n\nQuerying for '), data.getOutputs(i)
        ls.query(data.getSubWords(i))

    print('\nQuering with noise:')
    for i in range(data.getCount()):
        print('\n\nQuerying for '),data.getOutputs(i)
        ls.query(data.getSubWordsWithNoise(i))
# #Quering for unseen data:
#     print('Quering for unseen data')
#     for i in range(unseenData.getCount()):
#         ls.query(unseenData.getSubWords(i))
