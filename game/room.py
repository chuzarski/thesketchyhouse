
class Room():

    def __init__(self, label, title, desc, eLvl=0):
        self.__label = label
        self.__title = title
        self.__desc = desc
        self.__activities = dict()
        self.__exits = dict()
        self.__enemyLvl = eLvl

    def addActivity(self, activity):
        self.__activities[activity.getLabel()] = activity

    def addExit(self, exit):
        self.__exits[exit.getLabel()] = exit

    def getActivities(self):
        return self.__activities

    def getActivity(self, label):
        if label not in self.__activities:
            raise ValueError
        return self.__activities[label]

    def getEnemyLevel(self):
        return self.__enemyLvl

    def getExits(self):
        return self.__exits

    def getExit(self, label):
        if label not in self.__exits:
            raise ValueError
        return self.__exits[label]

    def hasExit(self, label):
        if label in self.__exits:
            return True
        else:
            return False

    def getLabel(self):
        return self.__label

    def setEnemyLevel(self, n):
        self.__enemyLvl = n

    def getTitle(self):
        return self.__title
    def getDescription(self):
        return self.__desc

    def populateItems(self):
        pass

    def hasActivity(self, label):
        if label in self.__activities:
            return True
        else:
            return False


    def getModel(self):

        model = dict()
        model["description"] = self.__desc
        model["list"] = self.__modelListString()

        return model

    def __modelListString(self):
        li = str()

        for a in self.__activities.values():
            li += "     go to: " + a.getLabel() + "  " + a.getTitle() + "\n"

        for e in self.__exits.values():
            li += "     go to: " + e.getLabel() + "\n"

        return li

    def getNavigateTarget(self, target):
        if self.hasExit(target):
            return "exit"
        elif self.hasActivity(target):
            return "activity"
        else:
            raise ValueError


class Activity():

    def __init__(self, label, title, desc):
        self.__label = label
        self.__description = desc
        self.__title = title
        self.__items = dict()

    def addItem(self, item):
        self.__items[item.getItemLabel()] = item

    def getItems(self):
        return self.__items

    def takeItem(self, label):

        item = None
        if label in self.__items:
            item = self.__items[label]
            self.__items.pop(label)
            return item
        else:
            return False

    def hasItem(self, label):
        if label in self.__items:
            return True
        else:
            return False

    def getDescription(self):
        return self.__description

    def getTitle(self):
        return self.__title

    def getLabel(self):
        return self.__label

    def getModel(self):

        model = dict()
        model["description"] = self.__description
        model["list"] = self.__itemListString()

        return model

    def __itemListString(self):

        li = str()

        for i in self.__items.values():
            li += i.getItemLabel() + " - " + i.getItemName() + " (qty: " + str(i.getItemQuantity()) + ")\n"
        return li

class RoomExit():
    """
    An exit is an object that encapsulates the room that the player can move to
    and the objectives that the player must meet to use the exit
    """

    def __init__(self, label, exitRoom, objectives):
        self.__objectives = objectives
        self.__exitTo = exitRoom
        self.__label = label

    def getObjectives(self):
        return self.__objectives
    def getExitTo(self):
        return self.__exitTo
    def getLabel(self):
        return self.__label
