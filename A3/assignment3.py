import numpy
import sys

class td_qlearning:

  alpha = 0.05
  gamma = 0.95

  def __init__(self, trial_filepath):
    # trial_filepath is the path to a file containing a trial through state space
    # Return nothing

  def qvalue(self, state, action):
    # state is a string representation of a state
    # action is a string representation of an action

    # Return the q-value for the state-action pair
    return q

  def policy(self, state):
    # state is a string representation of a state

    # Return the optimal action under the learned policy
    return a