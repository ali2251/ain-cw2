# mapAgents.py
# parsons/11-nov-2017
#
# Version 1.0
#
# A simple map-building to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is an extension of the above code written by Simon
# Parsons, based on the code in pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import sys

#
# A class that creates a grid that can be used as a map
#
# The map itself is implemented as a nested list, and the interface
# allows it to be accessed by specifying x, y locations.
#
class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

#
# An agent that creates a map.
#
# As currently implemented, the map places a % for each section of
# wall, a * where there is food, and a space character otherwise. That
# makes the display look nice. Other values will probably work better
# for decision making.
#
class MapAgent(Agent):

    # The constructor. We don't use this to create the map because it
    # doesn't have access to state information.
    def __init__(self):
        print "Running init!"

    # This function is run when the agent is created, and it has access
    # to state information, so we use it to build a map for the agent.
    def registerInitialState(self, state):
         print "Running registerInitialState!"
         # Make a map of the right size
         self.makeMap(state)
         self.addWallsToMap(state)
         self.updateFoodInMap(state)
         self.map.display()
         self.updateUtilities(api.walls(state), api.food(state), api.ghosts(state), 1000)
         self.counter = 0


    # This is what gets run when the game ends.
    def final(self, state):
        print "Looks like I just died!"

    # Make a map by creating a grid of the right size
    def makeMap(self,state):
        corners = api.corners(state)
        print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)
        
    # Functions to get the height and the width of the grid.
    #
    # We add one to the value returned by corners to switch from the
    # index (returned by corners) to the size of the grid (that damn
    # "start counting at zero" thing again).
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1

    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    # Functions to manipulate the map.
    #
    # Put every element in the list of wall elements into the map
    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], -5)

    # Create a map with a current picture of the food that exists.
    def updateFoodInMap(self, state):
        # First, make all grid elements that aren't walls blank.
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                if self.map.getValue(i, j) != -5:
                    self.map.setValue(i, j, -3)
        food = api.food(state)
        pacman = api.whereAmI(state)

        value = 100000
        foo = Directions.WEST
            #find closest food
    
        for i in range(len(food)):
            # for j in range(len(food)):
            #     temp = util.manhattanDistance(pacman,food[j])
            #     if temp < value:
            #         value = temp;
            #         foo = food[j]

       
            # val = 10 + value * -1   
            self.map.setValue(food[i][0], food[i][1], 10)
        


        
            
        # for ghost in api.ghosts(state):
        #     self.map.setValue(int(ghost[0]), int(ghost[1]), -20)    
    
    def updateGhosts(self, ghosts):
        for ghost in ghosts:
            g0 = int(ghost[0])
            g1 = int(ghost[1])
            self.map.setValue(g0,g1,-4)
            print "values now are ", self.map.getValue(g0,g1)
            print "values set to ", g0, " ", g1

    def getShortestGhostDistance(self, pacman, ghosts):
        
        if (len(ghosts) == 0):
            return 0

        minDistance = 10000
        for ghost in ghosts:
            temp = util.manhattanDistance(ghost, pacman)
            if temp < minDistance:
                minDistance = temp

        return minDistance


     
    def updateUtilities(self, walls, food, ghosts,num):

        change = True
        currentReward = 10

        # while change == True:

        for i in range(0,num):

            gemma = 1
            

            for i in range(self.map.getWidth()):
                for j in range(self.map.getHeight()):
                    current = self.map.getValue(i, j)
                    if current != -5:
                        alist = []
                        north1 = (i, j+1)
                        south1 = (i, j-1)
                        east = (i+1, j)
                        west = (i-1, j)
                        oldValue = self.map.getValue(i,j)
                        wallMap = dict()

                    


                      

                        values = []

                        alist.append(north1)
                        alist.append(south1)
                        alist.append(east)
                        alist.append(west)

                        for a in alist:
                            if a in walls:
                                wallMap[a] = True
                            else:
                                wallMap[a] = False

                          

                        for val in alist:
                            if val not in walls and val[0] < self.map.getWidth() and val[1] < self.map.getHeight():
                                
                                pNorth = 0.1
                                pSouth = 0.1
                                pEast = 0.1
                                pWest = 0.1

                                if wallMap[north1] == True:
                                    pNorth = 0.1 * self.map.getValue(val[0], val[1])
                                else:
                                    pNorth = 0.1 * self.map.getValue(north1[0], north1[1]) 

                                if wallMap[south1] == True:
                                    pSouth = 0.1 * self.map.getValue(val[0], val[1])
                                else:
                                    pSouth =  0.1 * self.map.getValue(south1[0], south1[1])

                                if wallMap[east] == True:
                                    pEast = 0.1 * self.map.getValue(val[0], val[1])
                                else:
                                    pEast = 0.1 * self.map.getValue(east[0],east[1])

                                if wallMap[west] == True:
                                    pWest = 0.1 * self.map.getValue(val[0], val[1])
                                else:
                                    pWest = 0.1 * self.map.getValue(west[0], west[1])


                                if val == west or val == east:
                                    temp =  0.8 * self.map.getValue(val[0], val[1]) + pSouth + pNorth
                                    values.append(temp)

                                if val == north1 or val == south1:
                                    temp =  0.8 * self.map.getValue(val[0],val[1]) + pEast + pWest 
                                    values.append(temp)
                                            
                        
                        #print(values , " -----------------------------------------")        
                                            
                        m = max(values)
                        rightBellman = gemma * m;
                        reward = -0.1
                        if (i,j) in food and self.map.getValue(i,j) != 10:
                            reward = 10
                        if (i,j) in ghosts:
                            reward = -10   

                            


                                

                        leftBellman = reward + rightBellman

                        if oldValue == leftBellman:
                            #print "----------------------old value and new value is the same-------------------"
                            change = False
                        else:
                            change = True    


                        self.map.setValue(i,j,leftBellman)    






                    # value = 100000
                    # collection = []
                    # foodDict = dict()
                    # foo = west
                    #     #find closest food
                
                    # for i in range(len(food)):
                    #     temp = util.manhattanDistance((i,j),food[i])
                    #     collection.append(temp)
                    #     foodDict[temp] = food[i] 
                    #     if temp < value:
                    #         value = temp;
                    #         foo = food[i]

                    # if value < closestDistance:
                    #     val = 10 + closestDistance * -1 * self.map.getValue(int(foo[0]),int(foo[1])) * gemma    
                    #     self.map.setValue(int(foo[0]),int(foo[1]), value)
                    #     closestDistance = value;


                    # if (i,j) in ghosts:
                    #     reward = -15
        # reward = self.map.getValue(move[0], move[1])
        #     print "reward is ===============", reward

        #     if mapOfLegal[move] == west:
        #         #north or south
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(northCoord[0], northCoord[1]) + 0.1 * self.map.getValue(southCoord[0], southCoord[1])
        #         moves.append((temp, west))

        #     if mapOfLegal[move] == south:
        #         #east or west
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(westCoord[0], westCoord[1]) + 0.1 * self.map.getValue(eastCoord[0], eastCoord[1])
        #         moves.append((temp, south))


        #     if mapOfLegal[move] == east:
        #         #north or south
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(northCoord[0], northCoord[1]) + 0.1 * self.map.getValue(southCoord[0], southCoord[1])
        #         moves.append((temp, east))


        #     if mapOfLegal[move] == north:
        #         #west or east
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(westCoord[0], westCoord[1]) + 0.1 * self.map.getValue(eastCoord[0], eastCoord[1])
        #         moves.append((temp, north))
       

 
    # For now I just move randomly, but I display the map to show my progress
    def getAction(self, state):
        #self.updateFoodInMap(state)
        self.map.prettyDisplay()

        self.counter = self.counter + 1



        walls = api.walls(state)
        corners = api.corners(state)
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)
        theFood = api.food(state)
        west = Directions.WEST
        east = Directions.EAST
        south = Directions.SOUTH
        north = Directions.NORTH
        ghostArray = api.ghosts(state)
        food = api.food(state)
        

        # if self.counter > 100 or len(food) <= 2:
        #     self.counter = 0
        self.updateUtilities(walls, theFood, ghostArray, 100)




        #self.updateGhosts(ghostArray)

        dist = self.getShortestGhostDistance(pacman, ghostArray)

        # if dist < 5 and dist != 0:
        #self.updateUtilities(walls, theFood, ghostArray)


        value = 100000
        mapOfWorld = dict()
        legalCoordinates = []
        mapOfLegal = dict()
        distances = []
        moves = []
        alist = []
        moveToCoordMap = dict()
        wallMap = dict()

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)


        


        westCoord = (pacman[0]-1, pacman[1])
        eastCoord = (pacman[0]+1, pacman[1])  
        northCoord =  (pacman[0], pacman[1]+1)
        southCoord = (pacman[0], pacman[1]-1)


        self.map.setValue(pacman[0],pacman[1], 1)

        for l in legal:
            if l == west:
                legalCoordinates.append(westCoord)
                mapOfLegal[westCoord] = west
                moveToCoordMap[west] = westCoord
            if l == east:
                legalCoordinates.append(eastCoord) 
                mapOfLegal[eastCoord] = east
                moveToCoordMap[east] = eastCoord
            if l == north:
                legalCoordinates.append(northCoord)
                mapOfLegal[northCoord] = north
                moveToCoordMap[north] = northCoord
            if l == south:
                legalCoordinates.append(southCoord)
                mapOfLegal[southCoord] = south
                moveToCoordMap[south] = southCoord          


        values = []

        alist.append(northCoord)
        alist.append(southCoord)
        alist.append(eastCoord)
        alist.append(westCoord)

        for a in alist:
            if a in walls:
                wallMap[a] = True
            else:
                wallMap[a] = False



          

        for val in alist:
            if val not in walls and val[0] < self.map.getWidth() and val[1] < self.map.getHeight():
                pNorth = 0.1
                pSouth = 0.1
                pEast = 0.1
                pWest = 0.1

                if wallMap[northCoord] == True:
                    pNorth = 0.1 * self.map.getValue(val[0], val[1])
                else:
                    pNorth = 0.1 * self.map.getValue(northCoord[0], northCoord[1]) 

                if wallMap[southCoord] == True:
                    pSouth = 0.1 * self.map.getValue(val[0], val[1])
                else:
                    pSouth =  0.1 * self.map.getValue(southCoord[0], southCoord[1])

                if wallMap[eastCoord] == True:
                    pEast = 0.1 * self.map.getValue(val[0], val[1])
                else:
                    pEast = 0.1 * self.map.getValue(eastCoord[0],eastCoord[1])

                if wallMap[westCoord] == True:
                    pWest = 0.1 * self.map.getValue(val[0], val[1])
                else:
                    pWest = 0.1 * self.map.getValue(westCoord[0], westCoord[1])


                if val == westCoord:
                    temp =  0.8 * self.map.getValue(val[0], val[1]) + pNorth + pSouth
                    values.append((temp, west))
                if val == eastCoord:
                    temp =  0.8 * self.map.getValue(val[0], val[1]) + pNorth + pSouth 
                    values.append( (temp,east ) )
                if val == northCoord:
                    temp =  0.8 * self.map.getValue(val[0],val[1]) + pEast + pWest 
                    values.append((temp, north))
                if val == southCoord:
                    temp =  0.8 * self.map.getValue(val[0],val[1]) + pEast + pWest 
                    values.append((temp, south))
                            
        

        #print(values , " -----------------------------------------")        
                            
        # m = max(values[0])
        # rightBellman = gemma * m;
        # reward = -1
        # if (i,j) in food:
        #     reward = 10 


                

        # leftBellman = reward + rightBellman

        #self.map.setValue(i,j,leftBellman)

        maximum = -10
        moveToMake = random.choice(legal)
      

        print moves

        for m in values:
            if m[0] > maximum:
                maximum = m[0]
                moveToMake = m[1]

        t = False
        for g in ghostArray:
            if moveToCoordMap[moveToMake] == g:
                t = True
    
        if t == False:
            direction = moveToMake
        else:
            print "++++++++++++++++++++++++++++++++++++++++"
            if (len(legal) > 1):
                legal.remove(moveToMake);
                direction = random.choice(legal)
            else:
                direction = moveToMake

        # print mapOfLegal        

        # for move in legalCoordinates:
        #     reward = self.map.getValue(move[0], move[1])
        #     print "reward is ===============", reward

        #     if mapOfLegal[move] == west:
        #         #north or south
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(northCoord[0], northCoord[1]) + 0.1 * self.map.getValue(southCoord[0], southCoord[1])
        #         moves.append((temp, west))     


        #     if mapOfLegal[move] == south:
        #         #east or west
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(westCoord[0], westCoord[1]) + 0.1 * self.map.getValue(eastCoord[0], eastCoord[1])
        #         moves.append((temp, south))


        #     if mapOfLegal[move] == east:
        #         #north or south
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(northCoord[0], northCoord[1]) + 0.1 * self.map.getValue(southCoord[0], southCoord[1])
        #         moves.append((temp, east))
        #         # for i in range(len(food)):
        #         #     temp = util.manhattanDistance(move,food[i])
        #         #     if temp < value:
        #         #         value = temp;
        #         #         foo = food[i]

        #         # distances.append((value, east))



        #     if mapOfLegal[move] == north:
        #         #west or east
        #         temp = reward + 0.8 * reward + 0.1 * self.map.getValue(westCoord[0], westCoord[1]) + 0.1 * self.map.getValue(eastCoord[0], eastCoord[1])
        #         moves.append((temp, north))

    



        # for d in distances:
        #     if d[0] < minimum:
        #         minimum = d[0]
        #         moveShould = d[1]



        print "--------------------> max is ", maximum

      
                   

        

        print "MEU Choice *****************", moveToMake

        # if maximum < 0:
        #     direction = random.choice(legal);

        #get the direction to go from getNextDirection
        # getNextDirection(pacman, self.corner, walls, legal, theFood, ghostArray)
        #return with a move
        return api.makeMove(direction, legal)



         # Random choice between the legal options.
        #return api.makeMove(random.choice(legal), legal)
    

   
