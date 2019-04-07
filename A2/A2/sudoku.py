#!/usr/bin/python3

import sys
import getopt
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = 24
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""
This course has been pretty interesting so far and as for the assignments,
they have been pretty challenging. I would like the instructions to be more
clear for instance, for the part1 it would have been nice to have a .cnf
example file. The most challenging topic is understanding and coding DPLL 
so far. I would also suggest having more instructor office hours if possible.
"""
#####################################################
#####################################################


def main(argv):
    inputfile = ''
    N = 0
    try:
        opts, args = getopt.getopt(argv, "hn:i:", ["N=", "ifile="])
    except getopt.GetoptError:
        print('sudoku.py -n <size of Sodoku> -i <inputputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
            sys.exit()
        elif opt in ("-n", "--N"):
            N = int(arg)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    instance = readInstance(N, inputfile)
    toCNF(N, instance, inputfile+str(N)+".cnf")


def readInstance(N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance = []
        for line in input_file:
            # Split the line on runs of whitespace
            number_strings = line.replace("\n", "").split()
            numbers = [int(n) for n in number_strings]  # Convert to integers
            if len(numbers) == N:
                instance.append(numbers)  # Add the "row" to your list.
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
        return instance  # a 2d list: [[1, 3, 4], [5, 5, 6]]


""" Question 1 """


def toCNF(N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"

    output_file.write("c {}\n".format(outputfile))
    output_file.write("p cnf {}\n".format(str(N*N*N)))

    nums = [x for x in range(1, N*N*N+1)]
    total_clauses = 0
    labels = []
    index = 0

    # each cell contains at least one copy of any number
    for i in range(0, N*N):
        labels.append([])
        for j in range(0, N):
            labels[i].append(nums[index])
            index += 1
        total_clauses += 1
        output_file.write(" ".join(str(v) for v in labels[i]) + " 0\n")

    # each cell contains at most one copy of any number
    for v in labels:
        for k in range(0, N):
            for l in range(0, N):
                if k != l:
                    total_clauses += 1
                    output_file.write("-{} -{} 0\n".format(v[k], v[l]))

    # each row contains every number exactly once
    for i in range(1, N+1):
        for k in range(1, N+1):
            for j in range(1, N):
                for l in range(j+1, N+1):
                    total_clauses += 1
                    num_1 = (N*N)*(i-1) + N*(j-1) + (k-1) + 1
                    num_2 = (N*N)*(i-1) + N*(l-1) + (k-1) + 1
                    output_file.write("-{} -{} 0\n".format(num_1, num_2))

    # each column contains every number exactly once
    for j in range(1, N+1):
        for k in range(1, N+1):
            for i in range(1, N):
                for l in range(i+1, N+1):
                    total_clauses += 1
                    num_1 = (N*N)*(i-1) + N*(j-1) + (k-1) + 1
                    num_2 = (N*N)*(l-1) + N*(j-1) + (k-1) + 1
                    output_file.write("-{} -{} 0\n".format(num_1, num_2))

    #  include constraints that restrict cells that were labeled in the puzzle grid
    lbl_idx = 0
    for item in instance:
        for sub_item in item:
            lbl_idx += 1
            if sub_item != 0:
                total_clauses += 1
                output_file.write("{} 0\n".format(
                    labels[lbl_idx - 1][sub_item - 1]))

    # edit line p
    output_file.close()
    with open(outputfile, 'r') as f:
        data = f.readlines()

    data[1] = data[1].replace("\n", " {}\n".format(str(total_clauses)))

    with open(outputfile, 'w') as f:
        f.writelines(data)

    "*** YOUR CODE ENDS HERE ***"
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])


"""
References:
1 - https://fania.uk/images/FaniaBSc.pdf
2 - https://media.readthedocs.org/pdf/pyeda/v0.27.3/pyeda.pdf
3 - https://github.com/jordanjay12/sudoku-solver/
"""
