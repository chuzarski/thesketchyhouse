from game.room import Room

__author__ = 'Cody Huzarski'


class Map():

    def __init__(self):
        self.__rooms = dict()
        self.__currRoom = ""
        self.__currActivity = ""

    def addRoom(self, room):
        self.__rooms[room.getLabel()] = room

    def getRoom(self, label):

        if label in self.__rooms:
            return self.__rooms[label]
        else:
            return False

    def getCurrentRoom(self):
        return self.__currRoom

    def getCurrentActivity(self):
        return self.__currActivity

    def setCurrentActivity(self, label):
        label = str(label)
        self.__currActivity = label

    def setCurrentRoom(self, label):
        label = str(label)
        self.__currRoom = label

    def populate(self, rList):
        for r in rList:
            self.addRoom(r)