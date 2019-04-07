#!/usr/bin/python3

import sys
import random
import math
import numpy as np

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 27
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
#
# Feedback: Assignments have been pretty engaging and interesting and piazza
# has been of great help. I would recommend adding more assignments like this
# and probably splitting assignment 2 into two assignments with similar level
# of difficulty. Lastly, I would like to say that making lecture notes more
# content-rich would be good as near exam preparation going through lecture
# videos does not seem feasible.
#####################################################
#####################################################


# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())


def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0


class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        # Start your code
        T = len(sequence)
        init_emission = self.emission[states[0]][sequence[0]]
        log_probs = np.zeros(T)

        log_probs[0] = math.log(self.prior[0]) + math.log(init_emission)
        for i in range(1, T):
            emission_prob = self.emission[states[i]][sequence[i]]
            transition_prob = self.transition[states[i-1]][states[i]]
            prev = log_probs[i-1]

            log_probs[i] = math.log(transition_prob) + \
                math.log(emission_prob) + prev

        return log_probs[T-1]
        # End your code
        ###########################################

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]

    def viterbi(self, sequence):
        ###########################################
        # Start your code

        T = len(sequence)
        D = self.num_states
        low_prior = math.log(self.prior[0])
        high_prior = math.log(self.prior[1])

        M0 = np.zeros([D, T])
        M1 = np.zeros([D, T])

        M0[0, 0] = low_prior + math.log(self.emission[0][sequence[0]])
        M0[1, 0] = high_prior + math.log(self.emission[1][sequence[0]])
        M1[0, 0] = 0
        M1[1, 0] = 0

        for i in range(1, T):
            for j in range(0, self.num_states):
                prev1 = M0[0][i-1]
                prev2 = M0[1][i-1]

                emission = self.emission[j][sequence[i]]

                transition_to_low = self.transition[0][j]
                transition_to_high = self.transition[1][j]

                low = math.log(transition_to_low) + prev1
                high = math.log(transition_to_high) + prev2
                max_prob = max(low, high)

                M0[j, i] = max_prob + math.log(emission)
                M1[j, i] = [low, high].index(max_prob)

        states = np.zeros(T, int)

        # get the most likely state
        states[T-1] = M0[:, T-1].argmax()

        for j in range(T-1, 0, -1):
            states[j-1] = M1[states[j], j]

        states_indicies = states.tolist()

        return states_indicies

        # End your code
        ###########################################


def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))


def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")


hmm = HMM()

file = sys.argv[1]
sequence = read_sequence(file)
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
name = file[:-4]+'_output.txt'
write_output(name, logprob, viterbi)


# References:
# 1 - https://stackoverflow.com/questions/9729968/python-implementation-of-viterbi-algorithm
