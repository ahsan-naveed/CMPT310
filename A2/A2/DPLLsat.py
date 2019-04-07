import random
import time
import copy
import getopt
import sys


class SatInstance:
    def __init__(self):
        pass

    def from_file(self, f):
        with open(f, "r") as input_file:
            self.VARS = set()
            self.clauses = list()
            for line in input_file:
                line = line.replace("\n", "")
                if line[0] not in ("p", "c"):
                    clause = Clause()
                    clause.from_str(line)
                    self.clauses.append(clause)
                    for VAR in clause.VARS:
                        self.VARS.add(VAR)
            self.VARS = sorted(self.VARS)

    def __str__(self):
        string_rep = ""
        for clause in self.clauses:
            string_rep += str(clause)
            string_rep += "\n"
        return string_rep


class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()[:-1]
        self.VARS = {}
        for token in s:
            if token[0] == "-":
                value = 0
                VAR = token[1:]
            else:
                value = 1
                VAR = token
            self.VARS[VAR] = value


def update_clauses(instance, VAR, value):
    new_clauses = list()
    instance = copy.deepcopy(instance)
    for clause in instance.clauses:
        if VAR in clause.VARS:
            if clause.VARS[VAR] == value:
                continue
            else:
                del clause.VARS[VAR]
        new_clauses.append(clause)
    instance.clauses = new_clauses
    return instance


def main(argv):
    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
    # -v sets the verbosity of informational output
    # (set to true for output veriable assignments, defaults to false)
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        model = solve_dpll(instance)
        if model == False:
            print("UNSAT")
        else:
            print("SAT")
        if model != False and verbosity == True:
            true_VARS = ""
            false_VARS = ""
            for VAR, value in list((model.items())):
                if value == 1:
                    true_VARS += " {}".format(VAR)
                else:
                    false_VARS += " -{}".format(VAR)
            print(true_VARS.strip())
            print(false_VARS.strip())

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


""" Question 2 """
# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#    list of false literals (if verbosity == True)
#
#  You will need to define your own
#  solve(VARS, F), pure-elim(F), propagate-units(F), and
#  any other auxiliary functions


def solve_dpll(instance, model=None):
    ###########################################
    # Start your code

    if model is None:
        model = {}
    if len(instance.clauses) == 0:
        return model
    for clause in instance.clauses:
        if len(clause.VARS) == 0:
            return False
    # stores indices of clauses for each VAR
    VARS_MAP = {VAR: list() for VAR in instance.VARS}
    for index, clause in enumerate(instance.clauses):
        for VAR in clause.VARS:
            VARS_MAP[VAR].append(index)

    # Unit Propagation
    for clause in instance.clauses:
        if len(clause.VARS) == 1:
            VAR, value = list(clause.VARS.items())[0]
            new_model = copy.deepcopy(model)
            new_model[VAR] = value
            new_instance = update_clauses(instance, VAR, value)
            return solve_dpll(new_instance, new_model)

    # Pure Literal Elimination
    for VAR in instance.VARS:
        if VAR in model:
            continue
        VAR_VALUES = set()
        for index in VARS_MAP[VAR]:
            VAR_VALUES.add(instance.clauses[index].VARS[VAR])
        if len(VAR_VALUES) == 1:
            value = list(VAR_VALUES)[0]
            new_model = copy.deepcopy(model)
            new_model[VAR] = value
            new_instance = update_clauses(instance, VAR, value)
            return solve_dpll(new_instance, new_model)

    # Recursive Backtracking
    VARS_NOT_ASSIGNED = set(instance.VARS) - set(model.keys())
    if len(VARS_NOT_ASSIGNED) == 0:
        raise Exception()

    # NOTE: we can choose VAR with minimum conflicts instead of
    # random walk. Checkout min_conflicts algorithm in book
    VAR = random.choice(list(VARS_NOT_ASSIGNED))

    # we use int values as they are faster to process instead
    # of boolean values i.e. for value in [True, False]:
    for value in [1, 0]:
        new_model = copy.deepcopy(model)
        new_model[VAR] = value
        new_instance = update_clauses(instance, VAR, value)
        ret = solve_dpll(new_instance, new_model)
        if ret != False:
            return ret
    return False
    # End your code
    ###########################################


if __name__ == "__main__":
    main(sys.argv[1:])

"""
References:
1 - http://www.cs.cornell.edu/courses/cs6862/2011sp/lec-04.pdf
2 - https://github.com/markankaro/dpll-sat
3 - https://github.com/jcwleo/DPLL-Algorithm
4 - https://github.com/Mihiro1ll1/SATsolver/blob/master/SAT.py
"""
