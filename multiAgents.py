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


from hashlib import new
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        # 2d array of food pellets left
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        score = successorGameState.getScore()


        "*** YOUR CODE HERE ***"

        # We reward being closer to dots.
        food_reward = 0.0
        count = 0
        for i in range(newFood.width):
          for j in range(newFood.height):
            if (newFood[i][j]):
              count+=1
              dist = manhattanDistance(newPos, (i, j))
              food_reward += (1.0/(dist)) * 4

        score += food_reward

        ghost_penalty = 0
        for ghost in newGhostStates:
          # Only do the penalty if they ghost isn't scared of us.
          if(ghost.scaredTimer == 0):
            ghost_pos = ghost.getPosition()
            pac_ghost_dist = manhattanDistance(newPos, ghost_pos)
            if(pac_ghost_dist == 0):
              ghost_penalty += 10000
            else:
              ghost_penalty += (1.0/(pac_ghost_dist)) * 7

        score -= ghost_penalty

        return score

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """


    # Assume there is at least one agent.
    def minimaxValue(self, gameState, depthLeft, currentAgentNum):
        """
          Minimax based off agents.
        """

        if (depthLeft == 0):
          return self.evaluationFunction(gameState)

      # We are pacman.
        if (currentAgentNum == 0):
          values = [self.minimaxValue(
                            gameState.generateSuccessor(currentAgentNum, action),
                            depthLeft,
                            currentAgentNum+1)  
                            for action in gameState.getLegalActions(currentAgentNum)]

          if (len(values) != 0 ):
            return max(values)
          else:
            return self.evaluationFunction(gameState)

        # Our agent is a minimum player.
        else: 
          # If we are the last minimum player, then we need to update total depth
          # allowing pacman to play again.
            if (currentAgentNum == gameState.getNumAgents() - 1):
                values = [self.minimaxValue(
                              gameState.generateSuccessor(currentAgentNum, action), 
                              depthLeft - 1,
                              0) 
                              for action in gameState.getLegalActions(currentAgentNum)]

                if (len(values) != 0):
                    return min(values)
                else:
                    return self.evaluationFunction(gameState)

            else: # Just a normal minumum player.
                values = [self.minimaxValue(
                            gameState.generateSuccessor(currentAgentNum, action),
                            depthLeft,
                            currentAgentNum+1)  
                            for action in gameState.getLegalActions(currentAgentNum)]

                if (len(values) != 0 ):
                    return min(values)
                else:
                    return self.evaluationFunction(gameState)

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
        "*** YOUR CODE HERE ***"

        bestAction = None
        bestValue = -1000000000
        for action in gameState.getLegalActions(0):
            value = self.minimaxValue(gameState.generateSuccessor(0, action), self.depth, 1)  

            if (value > bestValue):
                bestValue = value
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    # Based on Geek for geeks minimax
    # assume there is atleast one agent.
    def alphabeta(self, gameState, depthLeft, currentAgentNum, alpha, beta):
        """
          Minimax based off agents.
        """

        if (depthLeft == 0):
          return self.evaluationFunction(gameState)

      # We are pacman and are looking for the max value.
        if (currentAgentNum == 0):
          maxValue = -1000000000
          for action in gameState.getLegalActions(currentAgentNum):
            value = self.alphabeta(gameState.generateSuccessor(currentAgentNum, action),
                                       depthLeft, currentAgentNum+1, alpha, beta)  

            if (value > maxValue):
              maxValue = value

            if (maxValue > beta):
              return maxValue

            alpha = max(alpha, value)
        
          if (maxValue != -1000000000):
            return maxValue
          else:
            return self.evaluationFunction(gameState)

        # Our agent is a minimum.
        else: 
          # If we are the last minimum player, then we need to update total depth 
          # and go back to pacman.
            if (currentAgentNum == gameState.getNumAgents() - 1):
              minValue = 1000000000
              for action in gameState.getLegalActions(currentAgentNum):
                value = self.alphabeta(gameState.generateSuccessor(currentAgentNum, action),
                                       depthLeft - 1, 0, alpha, beta)  

                if (value < minValue):
                  minValue = value

                if (minValue < alpha):
                  return minValue

                beta = min(beta, value)
        
              if (minValue != 1000000000):
                return minValue
              else:
                return self.evaluationFunction(gameState)


            else: # Just a normal minumum.
              minValue = 1000000000
              for action in gameState.getLegalActions(currentAgentNum):
                value = self.alphabeta(gameState.generateSuccessor(currentAgentNum, action),
                                       depthLeft, currentAgentNum + 1, alpha, beta)  

                if (value < minValue):
                  minValue = value

                if (minValue < alpha):
                  return minValue

                beta = min(beta, value)
        
              if (minValue != 1000000000):
                return minValue
              else:
                return self.evaluationFunction(gameState)
  

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue = -1000000000
        alpha = -1000000000
        beta = 1000000000
        for action in gameState.getLegalActions(0):
            value = self.alphabeta(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta)  

            if (value > bestValue):
                bestValue = value
                bestAction = action

            if (bestValue > beta):
                return bestAction

            alpha = max(alpha, bestValue)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimaxValue(self, gameState, depthLeft, currentAgentNum):
        """
          Expectimax based off agents.
        """

        if (depthLeft == 0):
          return self.evaluationFunction(gameState)

      # We are pacman.
        if (currentAgentNum == 0):
          values = [self.expectimaxValue(
                            gameState.generateSuccessor(currentAgentNum, action),
                            depthLeft,
                            currentAgentNum+1)  
                            for action in gameState.getLegalActions(currentAgentNum)]

          if (len(values) != 0 ):
            return max(values)
          else:
            return self.evaluationFunction(gameState)

        # Our agent is a minimum.
        else: 
          # If we are the last minimum player, then we need to update total depth 
          # and go back to pacman.
            if (currentAgentNum == gameState.getNumAgents() - 1):
                actions = gameState.getLegalActions(currentAgentNum)
                values = [self.expectimaxValue(
                              gameState.generateSuccessor(currentAgentNum, action), 
                              depthLeft - 1,
                              0) 
                              for action in actions]

                if (len(values) != 0):
                    return sum(values) * (1.0/len(actions))
                else:
                    return self.evaluationFunction(gameState)

            else: # Just a normal minumum.
                actions = gameState.getLegalActions(currentAgentNum)
                values = [self.expectimaxValue(
                            gameState.generateSuccessor(currentAgentNum, action),
                            depthLeft,
                            currentAgentNum+1)  
                            for action in actions]

                if (len(values) != 0 ):
                    return sum(values) * (1.0/len(actions))
                else:
                    return self.evaluationFunction(gameState)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue = -1000000000
        for action in gameState.getLegalActions(0):
            value = self.expectimaxValue(gameState.generateSuccessor(0, action), self.depth, 1)  

            if (value > bestValue):
                bestValue = value
                bestAction = action

        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()

    # 2d array of food pellets left
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore() * 1.2

    # We reward being closer to dots.
    food_reward = 0.0
    
    for i in range(newFood.width):
      for j in range(newFood.height):
        if (newFood[i][j]):
          dist = manhattanDistance(newPos, (i, j))
          food_reward += (1.0/(dist)) * 3

    score += food_reward

    ghost_penalty = 0
    for ghost in newGhostStates:
      # Only do the penalty if they ghost isn't scared of us.
      if(ghost.scaredTimer == 0):
        ghost_pos = ghost.getPosition()
        pac_ghost_dist = manhattanDistance(newPos, ghost_pos)
        if(pac_ghost_dist == 0):
          ghost_penalty += 10000
        else:
          ghost_penalty += (1.0/(pac_ghost_dist)) * 6

    score -= ghost_penalty


    # This block gets the avg score up from 997.1 to 1000.8.
    ghost_eat = 0
    for ghost in newGhostStates:
      # Only do the penalty if they ghost isn't scared of us.
      if(ghost.scaredTimer > 0):
        ghost_pos = ghost.getPosition()
        pac_ghost_dist = manhattanDistance(newPos, ghost_pos)
        if(pac_ghost_dist != 0):
          ghost_eat += (1.0/(pac_ghost_dist)) * (30.0/ghost.scaredTimer)

    score += ghost_eat

    return score

# Abbreviation
better = betterEvaluationFunction

