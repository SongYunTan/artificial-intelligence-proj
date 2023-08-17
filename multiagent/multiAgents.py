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


import math
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        newFood_ls = newFood.asList()
        
        # print("food:",newFood_ls)
        # print("scared",newScaredTimes)
        "*** YOUR CODE HERE ***"
        ghost_dist = math.inf 
        food_dist = math.inf

        for i in range(len(newGhostStates)):
            x,y = newGhostStates[i].getPosition()
            if newScaredTimes[i] == 0:
                d = manhattanDistance((x,y),newPos)
                if d < ghost_dist:
                    ghost_dist = d
        
        for j in range(len(newFood_ls)):
            d = manhattanDistance(newFood_ls[j],newPos)
            if d < food_dist:
                food_dist = d
        
        run = 1/(ghost_dist-0.5)
        chase = 1/(food_dist+0.5)
        scoring = successorGameState.getScore() + chase - run

        return scoring

def scoreEvaluationFunction(currentGameState: GameState):
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        # print(gameState.getNumAgents())

        legalMoves = gameState.getLegalActions(0)
        scores = []
        
        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            scores.append(self.minimax(successor, 1, self.depth))
            
        bestAction = scores.index(max(scores))
        return legalMoves[bestAction]
        util.raiseNotDefined()
    
    def minimax(self, gameState: GameState, agentIndex, depth):
        if depth==0  or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []
        newIndex = (agentIndex+1)%gameState.getNumAgents()
        newDepth = depth-1 if newIndex == 0 else depth
        
        for action in legalMoves:
            successor = gameState.generateSuccessor(agentIndex, action)
            scores.append(self.minimax(successor, newIndex, newDepth))
        
        if agentIndex == 0:
            return max(scores)
        else:
            return min(scores)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        return self.minimax(gameState, 0, self.depth)[1]
        util.raiseNotDefined()

    def minimax(self, gameState: GameState, agentIndex, depth, alpha=-9999, beta=9999):
        if depth==0  or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []
        newIndex = (agentIndex+1)%gameState.getNumAgents()
        newDepth = depth-1 if newIndex == 0 else depth
        
        if agentIndex == 0:
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successor, newIndex, newDepth, alpha, beta)[0]
                scores.append(score)
                if score > beta:
                    return score, action
                alpha = max(alpha, score)
            bestAction = scores.index(max(scores))
            return max(scores), legalMoves[bestAction]
        else:
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.minimax(successor, newIndex, newDepth, alpha, beta)[0]
                scores.append(score)
                if score < alpha:
                    return score, action
                beta = min(beta, score)
            bestAction = scores.index(min(scores))
            return min(scores), legalMoves[bestAction]
    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.expectimax(gameState, 0, self.depth)[1]
        util.raiseNotDefined()
    
    def expectimax(self, gameState: GameState, agentIndex, depth):
        if depth==0  or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []
        newIndex = (agentIndex+1)%gameState.getNumAgents()
        newDepth = depth-1 if newIndex == 0 else depth
        
        if agentIndex == 0:
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                score = self.expectimax(successor, newIndex, newDepth)[0]
                scores.append(score)
                
            bestAction = scores.index(max(scores))
            return max(scores), legalMoves[bestAction]
        else:
            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, action)
                scores.append(self.expectimax(successor, newIndex, newDepth)[0])
            
            # chosenAction = random.randrange(0, len(scores))
            
            return sum(scores)/len(scores), None

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: evaluation function is the same as qn 1
    - found min ghost distance
    - found min food distance
    - 
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newFood_ls = newFood.asList()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    ghost_dist = math.inf 
    food_dist = math.inf

    for i in range(len(newGhostStates)):
        x,y = newGhostStates[i].getPosition()
        if newScaredTimes[i] == 0:
            d = manhattanDistance((x,y),newPos)
            if d < ghost_dist:
                ghost_dist = d
    
    for j in range(len(newFood_ls)):
        d = manhattanDistance(newFood_ls[j],newPos)
        if d < food_dist:
            food_dist = d
    
    run = 1/(ghost_dist-0.5)
    chase = 1/(food_dist+0.5)

    scoring = currentGameState.getScore() + chase - run
    # print(scoring)
    return scoring
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
