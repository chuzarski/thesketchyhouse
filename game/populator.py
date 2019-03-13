
import os, json
from game.enemy import Enemy
from game.items import Item
from game.room import Activity, RoomExit, Room


class Populator():

    def __init__(self, eng):

        # Paths for respective data items
        self.__DIRSEP = os.path.sep
        self.__PATH_ITEMS = "data"+self.__DIRSEP+"items"
        self.__PATH_ROOMS = "data"+self.__DIRSEP+"rooms"
        self.__PATH_ENEMIES = "data"+self.__DIRSEP+"enemies"
        self.__engineRef = eng


    def __resolvePath(self, p):
        """Gets an absolute path to the directory"""
        return os.getcwd() + self.__DIRSEP + p

    def __getFilePaths(self, dir):

        filePaths = list()

        for root, dirs, files in os.walk(dir):
            for f in files:
                if f.endswith(".json"):
                    filePaths.append(os.path.join(root, f))

        return filePaths

    def __retrieveJson(self, path):
        f = open(path, 'r')
        jDoc = json.load(f)
        f.close()
        return jDoc

    def __buildItemObject(self, jDoc):
        data = jDoc["item"]

        return Item(data["name"], data["label"], data["quantity"], data["usage"])


    def populateItems(self):
        items = list()
        dataFiles = self.__getFilePaths(self.__resolvePath(self.__PATH_ITEMS))

        for f in dataFiles:
            items.append(self.__buildItemObject(self.__retrieveJson(f)))

        return items

    def __buildActivityObject(self, act):

        activity = Activity(act["label"], act["title"], act["description"])
        iLabel = ""
        iQty = ""
        iProps = list()
        item = None

        for i in act["items"]:

            if "," in i:
                iProps = i.split(',')

                # First should be item label, next should be item qty
                iLabel = iProps[0]

                if len(iProps) == 2:

                    # First should be item label, next should be item qty
                    iLabel = iProps[0]
                    if iProps[1].isdigit():
                        iQty = int(iProps[1])
                    else:
                        iQty = 1

                    item = self.__engineRef.getItemLib().getItem(iLabel)
                    item.setQuantity(iQty)
                else:
                    item = self.__engineRef.getItemLib().getItem(i)
            else:
                item = self.__engineRef.getItemLib().getItem(i)

            activity.addItem(item)

        return activity

    def __buildExitObject(self, exObj):
        return RoomExit(exObj["label"], exObj["exitsTo"], exObj["objectives"])

    def __buildRoomObject(self, jDoc):
        data = jDoc["room"]

        activities = list()
        exits = list()
        room = None

        # assemble activities
        for a in data["activities"]:
            activities.append(self.__buildActivityObject(a))

        # assemble exits
        for e in data["exits"]:
            exits.append(self.__buildExitObject(e))

        # assemble room object
        room = Room(data["label"], data["title"], data["description"], data["enemyLevel"])

        # add all activities to the room
        for act in activities:
            room.addActivity(act)

        for ext in exits:
            room.addExit(ext)

        # that should be one inflated room
        return room

    def populateRooms(self):
        rooms = list()
        dataFiles = self.__getFilePaths(self.__resolvePath(self.__PATH_ROOMS))

        # populate the rooms
        for f in dataFiles:
            rooms.append(self.__buildRoomObject(self.__retrieveJson(f)))

        return rooms

    def __buildEnemyObject(self, jDoc):
        data = jDoc["enemy"]

        return Enemy(data["name"], data["label"], data["level"], float(data["damageRate"]))

    def populateEnemies(self):
        enemies = list()
        dataFiles = self.__getFilePaths(self.__resolvePath(self.__PATH_ENEMIES))

        for f in dataFiles:
            enemies.append(self.__buildEnemyObject(self.__retrieveJson(f)))

        return enemies

