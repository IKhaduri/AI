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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

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
    return  [s, s, w, s, w, w, s, w]


def fringe_search(problem, fringe):
    """
    standard search algorithm, stores full paths in fringe
    of the passed type, can work for bfs and dfs
    and doesn't re-visit any node that has already been
    marked.
    """
    marked = set()
    # stores state and path to state as a touple
    fringe.push((problem.getStartState(), []))
    while not fringe.isEmpty():
        cur = fringe.pop()
        if cur[0] in marked:
            continue
        marked.add(cur[0])
        if problem.isGoalState(cur[0]):
            return cur[1]
        else:
            for successor in problem.getSuccessors(cur[0]):
                if successor[0] not in marked:
                    fringe.push((successor[0], cur[1] + [successor[1]]))
    return []
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return fringe_search(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return fringe_search(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    marked = set()
    pq = util.PriorityQueue()
    # stores state and path to state as a touple
    # and cost as last argument. Starting cost is
    # 1, but it could be any number since this
    # priority queue takes different number of
    # arguments than stack and queue, it has been
    # written separately. Priority is being stored
    # too, because heap doesn't allow to view it
    pq.push((problem.getStartState(), [], 0), 0)
    while not pq.isEmpty():
        cur = pq.pop()
        if cur[0] in marked:
            continue
        marked.add(cur[0])
        if problem.isGoalState(cur[0]):
            return cur[1]
        else:
            for successor in problem.getSuccessors(cur[0]):
                if successor[0] not in marked:
                    pq.push((successor[0], cur[1] + [successor[1]], successor[2]+cur[2]), successor[2]+cur[2])
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """
    any element's priority is determined with its combined cost of path
    and heuristic evaluation.
    """
    pqf = util.PriorityQueueWithFunction(lambda x: heuristic(x[0], problem) + x[2])
    marked = set()
    pqf.push((problem.getStartState(), [], 1, 0))
    while not pqf.isEmpty():
        cur = pqf.pop()
        if cur[0] in marked:
            continue
        marked.add(cur[0])
        if problem.isGoalState(cur[0]):
            return cur[1]
        else:
            for successor in problem.getSuccessors(cur[0]):
                pqf.push((successor[0], cur[1] + [successor[1]], successor[2] + cur[2]))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
