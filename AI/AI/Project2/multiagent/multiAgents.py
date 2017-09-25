# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        currentGameState = currentGameState.generatePacmanSuccessor(action)
        position = currentGameState.getPacmanPosition()
        ghosts = currentGameState.getGhostStates()
        foods = currentGameState.getFood()
        foodScore = 0
        for x in foods.asList():
            foodScore = max(foodScore, 3.5 / manhattanDistance(x, position))
        ghostScore = 100000000
        for ghost in ghosts:
            ghostScore = min(ghostScore, manhattanDistance(position, ghost.getPosition()))
        if ghost.scaredTimer <= 0:
            ghostScore *= -1.0
            if ghostScore * (-1) <= 2:
                ghostScore = -10000000
            if ghostScore * (-1) < 5:
                ghostScore *= 15

        ghostScore *= 3.5
        return foodScore + ghostScore + currentGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
import time
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """



    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        numAgents = gameState.getNumAgents()
        maxDepth = self.depth

        def pacmanMove(depth, state):

            if state.isLose() or state.isWin() or depth == 0:
                return self.evaluationFunction(state), None
            res = -10000000000
            act = Directions.STOP
            # pacman tries to maximize
            for action in state.getLegalActions(0):
                tmp = ghostMove(1, depth, state.generateSuccessor(0, action))[0]
                if res < tmp:
                    res = tmp
                    act = action
            return res, act

        def ghostMove(ghostNum, depth, state):

            if state.isLose() or state.isWin():
                return self.evaluationFunction(state), None
            if ghostNum + 1 == numAgents:
                depth -= 1
            res = 10000000000
            act = Directions.STOP
            # ghosts try to minimize
            for action in state.getLegalActions(ghostNum):
                if ghostNum + 1 == numAgents:
                    tmp = pacmanMove(depth, state.generateSuccessor(ghostNum, action))[0]
                else:
                    tmp = ghostMove(ghostNum+1, depth, state.generateSuccessor(ghostNum, action))[0]
                if res > tmp:
                    res = tmp
                    act = action
            return res, act

        return pacmanMove(maxDepth, gameState)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        numAgents = gameState.getNumAgents()
        maxDepth = self.depth

        def pacmanMove(depth, state, alpha, beta):

            if state.isLose() or state.isWin() or depth == 0:
                return self.evaluationFunction(state), None
            res = -10000000000
            act = Directions.STOP
            # pacman tries to maximize
            for action in state.getLegalActions(0):
                tmp = ghostMove(1, depth, state.generateSuccessor(0, action), alpha, beta)[0]
                if res < tmp:
                    res = tmp
                    act = action
                if res > beta:
                    return res, act
                alpha = max(alpha, res)
            return res, act

        def ghostMove(ghostNum, depth, state, alpha, beta):

            if state.isLose() or state.isWin():
                return self.evaluationFunction(state), None
            if ghostNum + 1 == numAgents:
                depth -= 1
            res = 10000000000
            act = Directions.STOP
            # ghosts try to minimize
            for action in state.getLegalActions(ghostNum):
                if ghostNum + 1 == numAgents:
                    tmp = pacmanMove(depth, state.generateSuccessor(ghostNum, action), alpha, beta)[0]
                else:
                    tmp = ghostMove(ghostNum+1, depth, state.generateSuccessor(ghostNum, action), alpha, beta)[0]
                if res > tmp:
                    res = tmp
                    act = action
                if res < alpha:
                    return res, act
                beta = min(beta, res)
            return res, act

        return pacmanMove(maxDepth, gameState, -10000000000, 10000000000)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        numAgents = gameState.getNumAgents()
        maxDepth = self.depth

        def pacmanMove(depth, state):

            if state.isLose() or state.isWin() or depth == 0:
                return self.evaluationFunction(state), None
            res = -10000000000.0
            act = Directions.STOP
            # pacman tries to maximize
            for action in state.getLegalActions(0):
                tmp = ghostMove(1, depth, state.generateSuccessor(0, action))[0]
                if res < tmp:
                    res = tmp
                    act = action
            return res, act

        def ghostMove(ghostNum, depth, state):

            if state.isLose() or state.isWin():
                return self.evaluationFunction(state), None
            if ghostNum + 1 == numAgents:
                depth -= 1
            # ghosts try to minimize
            tmp = 0.0
            for action in state.getLegalActions(ghostNum):
                if ghostNum + 1 == numAgents:
                    tmp += pacmanMove(depth, state.generateSuccessor(ghostNum, action))[0]
                else:
                    tmp += ghostMove(ghostNum+1, depth, state.generateSuccessor(ghostNum, action))[0]
            return 1.000*tmp/len(state.getLegalActions(ghostNum)), None

        return pacmanMove(maxDepth, gameState)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    position = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    foods = currentGameState.getFood()
    foodScore = 0
    for x in foods.asList():
        foodScore = max(foodScore, 3.5 / manhattanDistance(x, position))
    ghostScore = 100000000
    for ghost in ghosts:
        ghostScore = min(ghostScore, manhattanDistance(position, ghost.getPosition()))
    if ghost.scaredTimer <= 0:
        ghostScore *= -1.0
        if ghostScore * (-1) < 5:
            ghostScore *= 15
    ghostScore *= 3.5
    return foodScore + ghostScore + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

