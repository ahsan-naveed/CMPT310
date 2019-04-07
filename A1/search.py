# search.py
# ---------
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


#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
import util
num_hours_i_spent_on_this_assignment = 9
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>

"""
#####################################################
#####################################################


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Questoin 1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    print (problem.isGoalState(problem.getStartState()) )
    print ( problem.getSuccessors(problem.getStartState()) )

    """
    "*** YOUR CODE HERE ***"
    exploredList = []
    actionsList = []

    # initialize the frontier using the initial state of the problem
    frontier = util.Stack()
    frontier.push((problem.getStartState(), actionsList))

    while frontier:
        # choose a leaf node and remove it from the frontier
        leafNode, actions = frontier.pop()

        if leafNode not in exploredList:
            # add the node to the explored set
            exploredList.append(leafNode)

            # if the node contains a goal state then return the corresponding solution
            if problem.isGoalState(leafNode):
                return actions

            # expand the chosen node and add the resulting nodes to the frontier
            leafNodeSuccessors = problem.getSuccessors(leafNode)

            for successor in leafNodeSuccessors:
                # successor[1] = direction
                # successor[0] = node
                actionsToTake = actions + [successor[1]]
                frontier.push((successor[0], actionsToTake))

    # return failure
    return []


def breadthFirstSearch(problem):
    """Questoin 1.2
     Search the shallowest nodes in the search tree first.
     """
    "*** YOUR CODE HERE ***"
    exploredList = []
    actionsList = []

    # initialize the frontier using the initial state of the problem
    frontier = util.Queue()
    frontier.push((problem.getStartState(), actionsList))

    while frontier:
        # choose a leaf node and remove it from the frontier
        leafNode, actions = frontier.pop()

        if leafNode not in exploredList:
            # add the node to the explored set
            exploredList.append(leafNode)

            # if the node contains a goal state then return the corresponding solution
            if problem.isGoalState(leafNode):
                return actions

            # expand the chosen node and add the resulting nodes to the frontier
            leafNodeSuccessors = problem.getSuccessors(leafNode)

            for successor in leafNodeSuccessors:
                # successor[1] = action
                # successor[0] = node
                actionsToTake = actions + [successor[1]]
                frontier.push((successor[0], actionsToTake))

    # return failure
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Question 1.3
    Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    exploredList = []
    actionsList = []
    probStartState = problem.getStartState()

    # initialize the frontier using the initial state of the problem
    frontier = util.PriorityQueue()
    frontier.push(
        (probStartState, actionsList),
        heuristic(probStartState, problem)
    )

    while frontier:
        # choose a leaf node and remove it from the frontier
        leafNode, actions = frontier.pop()

        if leafNode not in exploredList:
            # add the node to the explored set
            exploredList.append(leafNode)

            # if the node contains a goal state then return the corresponding solution
            if problem.isGoalState(leafNode):
                return actions

            # expand the chosen node and add the resulting nodes to the frontier
            leafNodeSuccessors = problem.getSuccessors(leafNode)

            for successor in leafNodeSuccessors:
                # successor[0] = node
                # successor[1] = action
                # successor[2] = stepCost
                actionsToTake = actions + [successor[1]]
                incrementalStepCost = problem.getCostOfActions(
                    actionsToTake) + heuristic(successor[0], problem)
                frontier.push(
                    (successor[0], actionsToTake), incrementalStepCost)

    # return failure
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch


#####################################################
############# Question no. 1.1: Answers #############
#####################################################
"""
# Answer no. 1
# Exploration order is as expected. DFS sticks with a
# path to the maximum depth before looking at another path.

# Answer no. 2
# Pacman does not go to all explored squares on the way to the goal.
# From all the explored paths only the path with goal node is followed  
# in our implementation. 

# Answer no. 3
# This is not the cheapest solution. DFS is an uninformed search and only 
# gives us the first path found to the goal node. First does not necessarily
# mean the best/cheapest path.
"""


#####################################################
############# Question no. 1.2: Answers #############
#####################################################
"""
# Answer no. 1
# Yes, BFS finds a cheaper solution as compared to the DFS. Total cost
# of mediumMaze with BFS is 68 and for DFS it is 130. This is because
# DFS does not necessarily look for the shortest/cheapest path.
"""


#####################################################
#################### Complexity #####################
#####################################################
"""
# Our heuristic is O(1) in the size of the maze. Euclidean
# distance is used as an heuristic and constant number of
# distance calculation performed using this heuristic is O(1)
# i.e. we compute distance between any two points without
# worrying about the size of the maze.
"""


#####################################################
################## Part 3 feedback ##################
#####################################################
"""
# What have I found most interesting:
# Assignments are very engaging.

# Topic that I had trouble understanding:
# This might not be a topic but presentations for written
# assignments in the class are hard to understand sometimes.

# Are there any changes that could improve the value of the course to me:
# When posting coding assignments it would be useful to show the
# lecture numbers or book sections that the student needs to do
# in order to solve the assignment completely.
"""

#####################################################
##################### References ####################
#####################################################

# http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
