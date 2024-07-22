#!/usr/bin/python
# -*- coding: utf-8 -*-
import pulp
from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    print("Number of items: ", item_count)

    # solve the problem
    decisions = [pulp.LpVariable(f"x_{item.index}", cat="Binary") for item in items]
    problem = pulp.LpProblem("Knapsack", pulp.LpMaximize)
    problem += sum(decision * item.value for decision, item in zip(decisions, items))
    problem += (
        sum(decision * item.weight for decision, item in zip(decisions, items))
        <= capacity
    )
    solver = pulp.getSolver("PULP_CBC_CMD", timeLimit=1.0, threads=8)
    solver_status = problem.solve(solver)

    # Check the status of the solution
    if pulp.LpStatus[solver_status] == "Optimal":
        print("Optimal solution found.")
    elif pulp.LpStatus[solver_status] == "Not Solved":
        print("Solver was not able to find a solution within the time limit.")
    else:
        print(f"Solver status: {pulp.LpStatus[solver_status]}")

    is_taken = [int(decision.varValue) for decision in decisions]
    value = sum(item.value * is_taken[item.index] for item in items)

    # prepare the solution in the specified output format
    output_data = str(value) + " " + str(0) + "\n"
    output_data += " ".join(map(str, is_taken))
    return output_data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"
        )
