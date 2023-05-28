import datetime

class Index:
    max_length = 100
    def __init__(self):
        self.index = []
        

    def addIndex(self, data: int):
        if len(self.index) >= max_length:
            return False
        self.index.append(data)
        return True

    def isFull(self):
        return len(index) > max_length

class IndexTable:
    def __init__(self):
        self.primaryIndex = Index()
        self.secondaryIndex = None
        self.thirdIndex = None

    def addIndex(data: int):
        if not self.primaryIndex.isFull():
            self.primaryIndex.addIndex(data)
            if self.primaryIndex.isFull():
                self.secondaryIndex = Index()
        elif not self.secondaryIndex.isFull():
            self.secondaryIndex.addIndex(data)
            if self.secondaryIndex.isFull():
                self.thirdIndex = Index()
        elif not thirdIndex.isFull():
            thirdIndex.addIndex(data)
        else:
            return False
        return True

    def readTable(self):
        res = self.primaryIndex.index
        if (not self.secondaryIndex) and self.primaryIndex.isFull():
            res += self.secondaryIndex.index
        if (not self.thirdIndex) and self.secondaryIndex.isFull():
            res += self.thirdIndex.index

        return res

class Block:
    max_length = 16
    def __init__(self):
        self.info = ''
        self.length = 0
        

    def setInfo(self, new_info):
        self.length = max_length if len(new_info) > max_length else len(new_info)
        self.info = new_info

class BasicFCB:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.modifiedTime = datetime.datetime.now()
        self.indexTable = IndexTable()

class SymFCB:
    cnt = 0
    def __init__(self, fileName = '', fileType = 'folder'):
        self.fileName = fileName
        self.fileType = fileType
        self.fileId = cnt
        cnt += 1
        self.father = None
        self.son = None
        self.next = None
        self.pre = None
    
    def addSon(self, newItem):
        if not self.son:
            self.son = newItem
            newItem.father = self
        else:
            temp = self.son
            while temp.next:
                temp = temp.next
            temp.next = newItem
            newItem.pre = temp
    def remove(self):
        if not self.pre:
            self.father.son = self.next
        else:
            self.pre.next = self.next
            self.next.pre = self.pre

class Catalog:
    def __init__(self):
        self.rootFCB = SymFCB()
    
class Pair:
    def __init__(self, sf = None, bf = None):
        self.symFCB = sf
        self.basicFCB = bf

class Manager:
    Capacity = 1e6
    def __init__(self):
        self.blocks = [None] * Capacity
        self.bitMap = [True] * Capacity
        self.bit_idx = 0

    def getBlock(self, i):
        return self.blocks[i].info

    def withdraw(self, *idxList):
        for idx in idxList:
            bitMap[idx] = True

    def allocBlock(self, data):
        self.bit_idx %= Capacity
        pointer = self.bit_idx
        while True:
            if self.bitMap[pointer]:
                self.blocks[pointer] = Block()
                self.blocks[pointer].setInfo(data)
                self.bit_idx = pointer + 1
                return pointer
            else:
                pointer = (pointer + 1) % Capacity
            
            if pointer == self.bit_idx:
                break
        return -1

    def writeData(self, data):
        table = IndexTable()
        while len(data) > IndexTable.max_length:
            table.addIndex(self.allocBlock(data[: IndexTable.max_length]))
            data = data[IndexTable.max_length: ]
        table.addIndex(self.allocBlock(data))
        return table