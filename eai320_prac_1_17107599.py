bfs_dfs = 0

# Author: Louw DM
# Student Number: 17107599
# Date Uploaded: Monday, 17 February 2020

# python rpsrunner.py eai320_prac_1_17107599.py,breakable.py

# It is possible to lose a match because the maximum number of plays, if the break sequence is the last node in a tree
# of depth 5, would be be ((3^1)*1)+((3^2)*2)+((3^3)*3)+((3^4)*4)+((3^5)*5) = 1641 rounds before it finds the
# break sequence, which means the break sequence would not be found when the maximum number of rounds played is 1000

# Self Comment: We will need to reset the breakSequence every match because their break sequences changes every match
# Self Comment: We will have to figure the break sequence and play the break sequence back to activate the repeat
# Self Comment: Their first play is random so will ours

# importing random as we do not have any data on the other player yet, so the first move in each match is always random
import random


# Class Node is used to build the tree, it holds the name of the vertex and an array of children (object)
# as well as a parent pointer to find the path
class Node:
    def __init__(self, name):
        self.name = name
        self.object = [None, None, None]
        self.parent = None


# Class Tree is used recursively build the tree made up of the Node Class
# The Tree is built up to a maximum depth of 5 which is excluding the "Start" Node
# Depth 5 is used
class Tree:
    def __init__(self):
        self.start = Node("Start")

    # Recursively builds tree up to the depth specified in the parameters
    # Setting each child of the current Node to me ["R", "P", "S"]
    # and also setting the child[i].parent = to current node, which sets the parent pointers
    def buildTree(self, size, nodePtr, curr):
        if size > 0:
            if nodePtr is None:
                self.start = None
                self.start = Node("Start")
                self.buildTree(size, self.start, self.start)

            else:
                curr = nodePtr
                nodePtr.object[0] = Node("R")
                nodePtr.object[1] = Node("P")
                nodePtr.object[2] = Node("S")
                # Creates a parents pointer
                nodePtr.object[0].parent = curr
                nodePtr.object[1].parent = curr
                nodePtr.object[2].parent = curr
                self.buildTree(size - 1, nodePtr.object[0], curr)
                self.buildTree(size - 1, nodePtr.object[1], curr)
                self.buildTree(size - 1, nodePtr.object[2], curr)

    # The BFS function is called on every new round which returns a queue of the next Nodes which need to be visited
    # so we do not loose track of our place in the tree in the middle of matches this does not return whole list of
    # the tree, only a queue to know which node to visit next such as if current node is "Start" it will return a
    # queue list of ["child[0] of current", child[1] of current, child[2] of current] or [Node "R", Node "P", Node "S"]
    def BFS(self, queue):
        # paths = []
        if not queue:
            return
        else:
            curr = queue.pop(0)

            if curr.object[0] is not None:
                queue.append(curr.object[0])
            if curr.object[1] is not None:
                queue.append(curr.object[1])
            if curr.object[2] is not None:
                queue.append(curr.object[2])

        return queue

    # The DFS function is called on every new round which returns a stack of the next Nodes which need to be visited
    # so we do not loose track of our place in the tree in the middle of matches this does not return whole list of
    # the tree, only a stack to know which node to visit next such as if current node is "Start" it will return a
    # stack list of ["child[0] of current", child[1] of current, child[2] of current] or [Node "R", Node "P", Node "S"]
    def DFS(self, stack):
        if not stack:
            return
        else:
            curr = stack.pop(0)

            if curr.object[2] is not None:
                stack.insert(0, curr.object[2])
            if curr.object[1] is not None:
                stack.insert(0, curr.object[1])
            if curr.object[0] is not None:
                stack.insert(0, curr.object[0])
        return stack


# The getPath function accepts any list of nodes that are in a stack (for DFS) or queue (for BFS)
# and then uses the parent pointers to traverse back up the path until start node is reached
# and then that path to the node is returned as a list such as ["R", "P", "S"], "R" representing
# the first level in the tree and so on
def getPath(q):
    if q:
        currNode = q[0]
        pathToNode = []

        # Builds the path from "Start" Node to Current Node, excluding the "Start" Node
        while currNode.parent is not None:
            pathToNode.insert(0, currNode.name)
            currNode = currNode.parent

        # Selects which Search the function must do depending on variable bfs_dfs
        if bfs_dfs == 0:
            q = tree5.BFS(q)
        else:
            q = tree5.DFS(q)

        return pathToNode
    else:
        return "Finished"


# playPath accepts and pathed list/None Empty list and and returns the objects "R", "P", or "S" depending on the path
# and the point in the paths which needs to be played
def playPath(path, i):
    pLen = len(path)
    if pLen != 0:
        return path[i]
    else:
        path = getPath(q)
        return playPath(path, i)


if input == "":
    # Builds tree on First Round to max depth of 5 as the maximum break sequence is 5 objects long
    tree5 = Tree()
    tree5.buildTree(5, None, None)

    # initializes counters to keep track of the place in the current path
    i = 0
    j = 0
    b = 0

    # Initialises the queue list or stack list to the "Start" Node which is then used in the functions DFS and BFS
    q = []
    curr = tree5.start
    q.append(curr)

    path = ""

    # Initialises history variable which stores the others bots past two plays
    hist = ["X"] * 2

    # Path queue store old paths that we have already traversed to we can access the most recent one
    pathQueue = ["X"]

    isBreakSequence = False
    repeatCounter = 0

    # Variable is used to store the break sequence if it is found
    breakSequence = ""

    # This will be first round so we make the first output to be random as we have no data to play on
    previous = random.choice(["R", "P", "S"])
else:
    # Store the most recent object the the other bot played
    hist.pop(0)
    hist.append(input)

    # If breakSequence is found it will firstly counter the repeated object
    if isBreakSequence:
        if hist[0] == hist[1]:
            # Plays the opposite of what is repeating
            if hist[1] == "R":
                previous = "P"
            elif hist[1] == "P":
                previous = "S"
            else:
                previous = "R"
        else:
            # If the breakSequence is found, after the repeat it replays the breakSequence again
            lenOfBreak = len(breakSequence)
            previous = playPath(breakSequence, j)
            j += 1
            if j >= lenOfBreak:
                j = 0
                repeatCounter += 1
            if repeatCounter == 1:
                isBreakSequence = False
                repeatCounter = 0
    # Continues on the next paths looking for a break
    else:
        if hist[0] == hist[1] and i == 1:
            # Sets sets a variable isBreakSequence to be true, to signal that a break is found
            # and store the breakSequence
            isBreakSequence = True
            breakSequence = pathQueue[0]

            if hist[1] == "R":
                previous = "P"
            elif hist[1] == "P":
                previous = "S"
            else:
                previous = "R"
        else:
            # If previous playas are not equal to each other then it must continue playing the paths
            # looking for a new break sequenc
            isBreakSequence = False

            if q:
                if i == 0:
                    if path is not None:
                        pathQueue.insert(0, path)
                    path = getPath(q)
                    pathLength = len(path)

                previous = playPath(path, i)

                i += 1
                if i >= pathLength:
                    i = 0

output = previous


# Output for BFS Search Tree:
# Pool 1: 2 bots loaded
# Playing 10 matches per pairing.
# Running matches in 12 threads
# 10 matches run
# total run time: 0.27 seconds
#
# breakable.py: won 0.0% of matches (0 of 10)
#     won 27.6% of rounds (2761 of 10000)
#     avg score -156.9, net score -1569.0
#
# eai320_prac_1_17107599.py: won 100.0% of matches (10 of 10)
#     won 43.3% of rounds (4330 of 10000)
#     avg score 156.9, net score 1569.0

# Output for DFS Search Tree:
# Pool 1: 2 bots loaded
# Playing 10 matches per pairing.
# Running matches in 12 threads
# 10 matches run
# total run time: 0.28 seconds
#
# breakable.py: won 0.0% of matches (0 of 10)
#     won 26.3% of rounds (2631 of 10000)
#     avg score -203.7, net score -2037.0
#
# eai320_prac_1_17107599.py: won 100.0% of matches (10 of 10)
#     won 46.7% of rounds (4668 of 10000)
#     avg score 203.7, net score 2037.0
