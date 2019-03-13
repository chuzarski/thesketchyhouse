from copy import deepcopy
from math import sqrt

class Enemy():

    def __init__(self, name, label, lvl, dmgRate=0.1):
        self.__name = name
        self.__label = label
        self.__health = 100.0
        self.__level = lvl
        self.__damageRate = dmgRate # used in conjunction with the level to determine enemy damage

    def getLabel(self):
        return self.__label

    def getHealth(self):
        return self.__health
    def getName(self):
        return self.__name
    def getLevel(self):
        return self.__level
    def getDamage(self):
        """
        Calculates damage per this graph:
        y = 2 * sqrt(lx) + 6r
        where:
        l - monster level
        r - rate (Monster difficulty)
        x - health
        :return:
        """

        l = self.__level
        r = self.__damageRate
        x = self.__health


        # Restrictions
        if r > 5:
            r = 5

        if l > 6:
            l = 6
        return 2 * sqrt(l*x) + (6*r)

    def updateHealth(self, val):
        # Typically we are subtracting health from the enemy
        if (self.__health - val) <= 0:
            self.__health = 0 # just default enemy health to 0
        else:
            self.__health = self.__health - val # just subtract the amount

class EnemyLibrary():

    def __init__(self):
        self.__lib = dict()

    def addEnemy(self, obj):
        self.__lib[obj.getLabel()] = obj

    def getEnemy(self, label):
        return self.__lib[label]

    def getEnemyCopy(self, label):
        return deepcopy(self.__lib[label])

    def populate(self, eList):
        for e in eList:
            self.addEnemy(e)

    def genEnemyList(self, lvl):
        lvl = int(lvl)
        li = list()

        # loop through the dictionary, if an enemy has a matching level, add it to the list
        for e in self.__lib.values():
            if e.getLevel() == lvl:
                li.append(e)

        return li

class encounterState():

    def __init__(self, enemy, moveTarget, moveTargetType):

        self.__complete = False
        self.__enemy = enemy
        self.__originalmovetarget = moveTarget
        self.__moveTargetType = moveTargetType
        self.__actionMessage = list()

    def isComplete(self):
        return self.__complete

    def setcomplete(self, val=False):
        self.__complete = val

    def setenemy(self, enemy):
        self.__enemy = enemy

    def getEnemy(self):
        return self.__enemy

    def getMoveTarget(self):
        return self.__originalmovetarget

    def getMoveType(self):
        return self.__moveTargetType

    def addActionMessage(self, msg):
        self.__actionMessage.append(msg)

    def damage(self, val):
        # Basically subtract val from enemy health
        self.__enemy.updateHealth(val)


    def getModel(self):
        data = dict()
        data["actionMessage"] = self.__actionMessage
        data["health"] = self.__enemy.getHealth()
        data["name"] = self.__enemy.getName()
        return data