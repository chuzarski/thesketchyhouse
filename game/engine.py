from game.enemy import EnemyLibrary, encounterState
from game.items import ItemLibrary
from game.map import Map
from game.player import Player
from game.populator import Populator
from game.util import *
from random import randint
from copy import deepcopy


class Engine():

    def __init__(self):

        # GAME STATE
        self.__map = Map()
        self.__player = Player()
        self.__encounterState = None

        # Libraries
        self.__itemLib = ItemLibrary()
        self.__enemyLib = EnemyLibrary()

        # RUNNING STATE
        self.stateFlags = ("quit", "won", "dead", "running")
        self.__stateFlag = self.stateFlags[3] # defaults to running

        # COMMANDS
        self.__general_commands = ("goto", "back")
        self.__combat_commands = ("attack", "defend", "escape")
        self.__inventory_commands = ("drop", "use", "take", "showinventory")
        self.__gamestate_commands = ("quit",  "#!")
        self.__inputTokens = []
        self.__statusLine = ""

        # VIEW STATE
        self.__viewStateFlags = ("room", "encounter", "activity", "inventory")
        self.__viewState = list()

        #FLAGS
        self.__FLAG_NEW_GAME = True
        self.__BOSS_FIGHT = False

        self.initGame()


    def __initPopulate(self):

        """
        This function will populate the Item Library, Rooms in the map, Activities/exits in the rooms
        It does this by creating a Populator object which loads JSON files and creates the individual objects as
        a result
        """
        p = Populator(self)

        # Populate item library
        self.__itemLib.populate(p.populateItems())

        # Populate the map
        self.__map.populate(p.populateRooms())

        # Populate enemies
        self.__enemyLib.populate(p.populateEnemies())

        # kill the object
        p = None

    def initGame(self):

        """
        Sets up the engine for a game
        :return:
        """

        # Populate everything
        self.__initPopulate()

        self.__newGameInit()

    def __newGameInit(self):

        """
        Sets values for a fresh new game
        :return:
        """
        self.__map.setCurrentRoom("basement")
        self.__viewState.append(self.__viewStateFlags[0])

        self.__FLAG_NEW_GAME = False

    def takeInput(self):

        """
        Takes input from the player and sets the command tokens
        :return:
        """

        # Fixed a problem with prompting user AFTER they have quit
        if self.__stateFlag == self.stateFlags[0]:  # Player has quit
            return True

        self.__inputTokens = tokenize(input(": "))

    def update(self):

        """
        All the magic happens in this function. update will take the command tokens, delegate
        which function will handle the command. Then this will call the function to update that output
        that represents the game state
        :return:
        """

        # delegate to specific parsing function
        if len(self.__inputTokens) > 0:
            if self.__inputTokens[0] in self.__general_commands:
                self.__parseGeneral()
            elif self.__inputTokens[0] in self.__combat_commands:
                self.__parseCombat()
            elif self.__inputTokens[0] in self.__inventory_commands:
                self.__parseInventory()
            elif self.__inputTokens[0] in self.__gamestate_commands:
                self.__parseGamestate()
            else:
                self.__statusLine = "What command are you trying?"

            # flush input - we do not the commands from the last pass
            self.__inputTokens.clear()

        # do not show the results when we quit the game.
        if self.__stateFlag == self.stateFlags[0]:  # Player has quit
            return True

        self.__playerDeathCheck()

        #show the results
        self.__updateOut()


    ### PARSING FUNCTIONS

    def __parseGeneral(self):

        """
        Parses the command line for any commands that are "general" commands
        and delegates it to its handler
        :return:
        """
        if self.__inputTokens[0] == self.__general_commands[0]:  # goto command
            self.__processGoTo(self.__inputTokens[1])
        elif self.__inputTokens[0] == self.__general_commands[1]:
            self.__goBack()

    def __parseCombat(self):

        if self.__inputTokens[0] == self.__combat_commands[0]: # Attack command
            self.__attackEnemy()

    def __parseInventory(self):
        """
        Parses the command line for any commands that are "inventory" commands
        and delegates it to its handler
        :return:
        """

        if self.__inputTokens[0] == self.__inventory_commands[2]:
            self.__takeItem(self.__inputTokens[1])
        elif self.__inputTokens[0] == self.__inventory_commands[3]:
            self.__showInventory()
        elif self.__inputTokens[0] == self.__inventory_commands[0]:
            self.__dropItem(self.__inputTokens[1])
        elif self.__inputTokens[0] == self.__inventory_commands[1]:
            self.__useItem(self.__inputTokens[1])
            pass

    def __parseGamestate(self):
        """
        This will handle gamestate such as quit, commands outside the games (i.e. cheat commands)
        :return:
        """
        # TODO implement cheats
        if self.__inputTokens[0] == "quit":
            self.__stateFlag = self.stateFlags[0]

    def getStateFlag(self):
        return self.__stateFlag

    ################################################
    ###     Command Processors                  ###
    ################################################

    ## Movement commands

    def __processGoTo(self, target):

        room = self.__map.getRoom(self.__map.getCurrentRoom())
        destType = None

        if self.__checkEncounterState() == "fight":
            self.__statusLine = "You cannot move anywhere when in a fight"
            return False

        try:
            destType = room.getNavigateTarget(target)
        except ValueError:
            self.__statusLine = target + " is an incorrect destination"
            return False

        if self.__generateEncounter(target, destType):
            return False
        else:
            if destType == "activity":
                self.__navActivity(target)
            elif destType == "exit":
                self.__navExit(target)
        return True

    def __navActivity(self, target):

        """
        modifies the position of the player to be at an activity within a level
        :param target: label of the activity to move to
        :return:
        """

        room = self.__map.getRoom(self.__map.getCurrentRoom())

        if room.hasActivity(target):
            self.__map.setCurrentActivity(target)
            self.__viewState.append(self.__viewStateFlags[2])
        else:
            self.__statusLine = target + " is not a valid activity."

    def __navExit(self, target):
        """
        performs the movement of the player into another room
        :param target:
        :return:
        """

        room = self.__map.getRoom(self.__map.getCurrentRoom())
        ex = None

        if room.hasExit(target):
            # get the exit object
            ex = room.getExit(target)
        else:
            self.__statusLine = target + " is not a valid exit"
            return False

        # can the player exit?
        if not ex.getObjectives() == "":
            # check that the player has this one item
            # TODO support multiple items here
            if not self.__player.getPlayerInventory().hasItem(ex.getObjectives()):
                self.__statusLine = "Player does not have a " + ex.getObjectives()
                return False

        # checks passed, change the room and the viewstate
        self.__map.setCurrentRoom(ex.getExitTo())
        self.__map.setCurrentActivity("")
        self.__viewState.clear()
        self.__viewState.append(self.__viewStateFlags[0])
        # TODO possibly make a reset function


    ### Encounters

    def __generateEncounter(self, target, targetType):

        oddFactor = 0

        # generate our odd factor
        if self.__map.getRoom(self.__map.getCurrentRoom()).getEnemyLevel() == 6: # This is a boss fight
            oddFactor = 1
            self.__BOSS_FIGHT = True
        else:
            oddFactor = randint(0, 3) # good odds right?

        # first of all.. Should we have an enemy?
        if oddFactor == 1:
            # get an enemy
            enemy = self.__spawnEnemy()

            if enemy == False:
                return False

            # set an encounter state
            self.__encounterState = encounterState(enemy, target, targetType)

            # set the viewstate to encounter
            self.__viewState.append(self.__viewStateFlags[1]) # encounter state

            return True
        else:
            return False


    def __checkEncounterState(self):

        if self.__encounterState == None:
            return False
        else:
            if self.__encounterState.isComplete() == False:
                return "fight"
            else:
                self.__encounterState = None
                return True

    def __spawnEnemy(self):

        # get the current room level
        lvl = self.__map.getRoom(self.__map.getCurrentRoom()).getEnemyLevel()
        enemies = None
        enemy = None
        eIdx = 0

        # get possible canidates
        enemies = self.__enemyLib.genEnemyList(lvl)

        if len(enemies) == 0:
            return False
        else:
            # now get a random enemy
            eIdx = randint(0, len(enemies) - 1)
            enemy = enemies[eIdx]

        return deepcopy(enemy)


    def __attackEnemy(self):

        # Check that we are in a fight
        if not self.__checkEncounterState() == "fight":
            self.__statusLine = "You are not in a fight"
            return False

        # calculate damage
        dmg = self.__player.getHealth() * .5 # Player causes 1/2 of their health as damage

        # update the enemy health
        self.__encounterState.damage(dmg)

        # add to message
        self.__encounterState.addActionMessage("You have attacked the enemy causing %.2f damage!" % dmg)

        self.__enemyResponse()


    def __enemyResponse(self):

        # Is the enemy dead?
        if self.__encounterState.getEnemy().getHealth() == 0: # kill the encounter
            self.__encounterState.setcomplete(True)
            self.continueFromEncounter(self.__encounterState.getMoveTarget(), self.__encounterState.getMoveType())
            self.__statusLine = "You have destroyed the " + self.__encounterState.getEnemy().getName()
            return True

        eDmg = self.__encounterState.getEnemy().getDamage()
        # make the enemy attack the player
        if self.__player.deductHealth(eDmg):
            self.__encounterState.addActionMessage("You were attacked causing %.2f damage!" % eDmg)

    def __handleBossDefeat(self):
        # player has defeated the boss, shut off boss fight
        if self.__BOSS_FIGHT == True and self.__map.getCurrentRoom() == "sunroom":
            self.__map.getRoom("sunroom").setEnemyLevel(0)

    ##      INVENTORY RELATED
    def __takeItem(self, label):
        """
        This function performs the taking of an item by a player from an activity
        :param label:
        :return:
        """

        a = self.__map.getRoom(self.__map.getCurrentRoom()).getActivity(self.__map.getCurrentActivity())
        item = None
        # check that the activity has the item
        if a.hasItem(label):
            self.__player.getPlayerInventory().addItem(a.takeItem(label))
        else:
            self.__statusLine = "That item is not here!"
            return False

    def __showInventory(self):
        # simply change the view to the inventory state
        self.__viewState.append(self.__viewStateFlags[3])

    def __dropItem(self, label):
        """
        perfroms the dropping of an item from the player inventory
        :param label:
        :return:
        """
        pi = self.__player.getPlayerInventory()
        if pi.hasItem(label):
            pi.removeItem(label)
            self.__statusLine = "You dropped: " + label
        else:
            self.__statusLine = "You do not have that item"


    def __useItem(self, label):

        if label == "healthkit":
            # check if the player has a healthkit
            if self.__player.getPlayerInventory().hasItem("healthkit"):
                # add the player health
                self.__player.addHealth(30) # healthkits always restore 30
                # use the item
                self.__player.getPlayerInventory().useItem("healthkit")
            else:
                self.__statusLine = "You do not have a health kit"
        else:
            self.__statusLine = "Item is not usable"

    ################################################
    ###     MISC                                ###
    ################################################


    def __playerDeathCheck(self):
        if self.__player.getHealth() == 0:
            self.__stateFlag = self.stateFlags[2]

    def continueFromEncounter(self, target, type):

        # remove the encounter from the viewstack
        self.__viewState.pop()

        if type == "exit":
            self.__navExit(target)
        elif type == "activity":
            self.__navActivity(target)


    def __goBack(self):
        """
        This function will go BACK to the previous view state in the view state stack
        :return:
        """

        if self.__checkEncounterState() == "fight": # Player is CURRENTLY in an encounter
            # Are they in their inventory?
            if self.__getViewState() == self.__viewStateFlags[3]:
                self.__viewState.pop()
            else:
                self.__statusLine = "You cannot leave a fight"
                return False

        if len(self.__viewState) > 1:
            self.__viewState.pop()
        else:
            self.__statusLine = "You cannot go back further!"
            return False

    ################################################
    ###     OUTPUT RELATED METHODS              ###
    ################################################

    def __updateOut(self):
        """
        Always called on update. This updates the output of the engine according to the view state
        :return:
        """
        clearScn()
        self.__outHeading()

        if self.__stateFlag == self.stateFlags[2]: # The player is dead. Game over.
            self.__outGameDeath()
            return True

        # determine view state
        if self.__getViewState() == self.__viewStateFlags[0]: # A room
            self.__outRoom()
        elif self.__getViewState() == self.__viewStateFlags[2]: # An activity
            self.__outActivity()
        elif self.__getViewState() == self.__viewStateFlags[3]: # Inventory
            self.__outInventory()
        elif self.__getViewState() == self.__viewStateFlags[1]: # encounter
            self.__outEncounter()

        return True

    def __outGameDeath(self):
        print("Good try! You are dead. This is the end. type quit and try again.")
        print("Have a great day :)")

    def __outHeading(self):
        #Print current level
        print(self.__map.getRoom(self.__map.getCurrentRoom()).getTitle())

        #Print player Health
        print("Player Health: %.2f" % self.__player.getHealth())

        if not self.__statusLine == "":
            # There is a message to print
            print(self.__statusLine)
            self.__statusLine = ""
        print()

    def __outRoom(self):
        model = self.__map.getRoom(self.__map.getCurrentRoom()).getModel()
        if not self.__player.hasVisited(self.__map.getCurrentRoom()):
            typewrite(model["description"])

            try:
                self.__player.visit(self.__map.getCurrentRoom())
            except ValueError:
                self.__statusLine = "Internal error occured - __outRoom()"
        else:
            print(model["description"])

        print(model["list"])

    def __outInventory(self):

        print("\n" + self.__player.getPlayerInventory().getModel())


    def __outActivity(self):

        model = self.__map.getRoom(self.__map.getCurrentRoom()).getActivity(self.__map.getCurrentActivity()).getModel()

        print(model["description"])
        print()
        print(model["list"])

    def __outEncounter(self):
        model = self.__encounterState.getModel()

        print("You have encountered a " + model["name"] + "\n\n")

        for am in model["actionMessage"]:
            # print each action message
            print("  * " + am)

        print("Enemy Health: %.2f" % model["health"])

    def __getViewState(self):
        idx = len(self.__viewState) - 1 # our current view state
        return self.__viewState[idx]

    # GETTERS

    def getItemLib(self):
        return self.__itemLib