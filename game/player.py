from game.items import Item

class Player():

    def __init__(self):
        self.__health = 100
        self.__inventory = PlayerInventory()
        self.__metObjectives = list()
        self.__currLevel = ""
        self.__visited = list()

    def addHealth(self, n):

        if self.__health == 100:
            return False
        elif self.__health < self.__health + 100:
            self.__health = self.__health + (n - 100)
        else:
            self.__health = self.__health + n
            return True

    def getHealth(self):
        return self.__health

    def addHealth(self, val):
        # Typically we are subtracting health from the enemy
        if (self.__health + val) >= 100:
            self.__health = 100
        else:
            self.__health = self.__health + val # just subtract the amount

    def hasVisited(self, label):
        if label in self.__visited:
            return True
        else:
            return False

    def visit(self, label):
        if label in self.__visited:
            raise ValueError
        else:
            self.__visited.append(label)

    def deductHealth(self, n):

        if self.__health == 0:
            return False
        elif self.__health - n <= 0:
            self.__health = 0
            return False
        else:
            self.__health = self.__health - n
            return True
    def getPlayerInventory(self):
        return self.__inventory


class PlayerInventory():

    def __init__(self):
        self.__i = dict()

    def addItem(self, item):

        if self.hasItem(item.getItemLabel()):
            # increment the item count
            self.__i[item.getItemLabel()].updateQuantity(item.getItemQuantity())
        else:
            self.__i[item.getItemLabel()] = item

    def getInventoryCount(self):
        return len(self.__i)

    def hasItem(self, label):
        if label in self.__i:
            return True
        else:
            return False

    def removeItem(self, label):
        self.__i.pop(label)

    def useItem(self, label):

        if self.__i[label].getItemQuantity() > 1:
            self.__i[label].updateQuantity(-1)
        else:
            self.removeItem(label)


    def getModel(self):

        li = "Inventory: \n"

        for i in self.__i.values():
            li += "    " + i.getItemLabel() + " (qty: " + str(i.getItemQuantity()) + ")\n"

        return li