from copy import deepcopy


class Item():

    def __init__(self, name, label, quantity, use=""):
        self.__name = name
        self.__label = label
        self.__quantity = quantity
        self.__usage = use

    def getItemName(self):
        return self.__name

    def setItemName(self, name):
        name = str(name)
        self.__name = name

    def getUsage(self):
        return self.__usage

    def isUsable(self):
        if self.__usage == "":
            return False
        else:
            return True

    def getItemQuantity(self):
        return self.__quantity

    def updateQuantity(self, n):
        self.__quantity = self.__quantity + n

    def setQuantity(self, val):
        self.__quantity = val

    def getItemLabel(self):
        return self.__label

class ItemLibrary():

    def __init__(self):
        self.__allitems = dict()

    def addItem(self, item):
        self.__allitems[item.getItemLabel()] = item
    def getItem(self, label):
        if label in self.__allitems:
            return deepcopy(self.__allitems[label])
        else:
            print("Failure to retrieve item because it does not exist: " + label)
            raise ValueError

    def populate(self, iList):
       for i in iList:
           self.addItem(i)
