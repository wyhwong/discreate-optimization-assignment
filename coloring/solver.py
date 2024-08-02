#!/usr/bin/python
# -*- coding: utf-8 -*-
import pulp


def check_solver_status(solver_status):

    # Check the status of the solution
    if pulp.LpStatus[solver_status] == "Optimal":
        print("Optimal solution found.")
    elif pulp.LpStatus[solver_status] == "Not Solved":
        print("Solver was not able to find a solution within the time limit.")
    else:
        print(f"Solver status: {pulp.LpStatus[solver_status]}")


def get_optimal_solution_1(node_count, edges):
    """Get optimal solution for the graph coloring problem
    This method uses integer variables to represent the color of each node.
    The objective is to minimize the number of colors used.
    """

    problem = pulp.LpProblem("Graph Coloring", pulp.LpMinimize)
    decisions = [
        pulp.LpVariable(
            f"node_color_{i}", cat="Integer", lowBound=0, upBound=node_count - 1
        )
        for i in range(node_count)
    ]
    n_colors_used = pulp.LpVariable(
        "n_colors_used",
        cat="Integer",
        lowBound=1,
        upBound=node_count,
    )

    problem += n_colors_used

    for i in range(node_count):
        # constraint: n_colors_used must be at least the maximum color index used
        problem += n_colors_used - decisions[i] >= 0

    # constraint: adjacent nodes must have different colors
    # Here we need to transform the constraint to be a linear constraint
    binds = [pulp.LpVariable(f"bind_{i}", cat="Binary") for i in range(len(edges))]
    for i, j in edges:
        problem += decisions[j] - decisions[i] + node_count * binds[i] >= 1
        problem += decisions[i] - decisions[j] + node_count * (1 - binds[i]) >= 1

    solver = pulp.getSolver("PULP_CBC_CMD", timeLimit=90.0, threads=8)
    solver_status = problem.solve(solver)
    check_solver_status(solver_status)
    solution = [int(abs(decision.varValue)) for decision in decisions]
    return solution


def get_optimal_solution_2(node_count, edges):
    """Get optimal solution for the graph coloring problem
    This method uses binary variables to represent the color of each node.
    The objective is to minimize the number of colors used.
    """

    problem = pulp.LpProblem("Graph Coloring", pulp.LpMinimize)
    decisions = [
        [
            pulp.LpVariable(f"is_node{i}_filled_color{j}", cat="Binary")
            for j in range(i + 1)
        ]
        for i in range(node_count)
    ]
    n_colors_used = pulp.LpVariable(
        "n_colors_used",
        cat="Integer",
        lowBound=1,
        upBound=node_count,
    )

    problem += n_colors_used

    for i in range(node_count):
        # constraint: each node must be assigned exactly one color
        problem += pulp.lpSum(decisions[i][j] for j in range(i + 1)) == 1

        # constraint: n_colors_used must be at least the maximum color index used
        for j in range(i + 1):
            problem += n_colors_used - decisions[i][j] * j >= 0

    for i, j in edges:

        for k in range(min(i, j) + 1):
            # constraint: adjacent nodes must have different colors
            problem += decisions[i][k] + decisions[j][k] <= 1

    solver = pulp.getSolver("PULP_CBC_CMD", timeLimit=90.0, threads=8)
    solver_status = problem.solve(solver)
    check_solver_status(solver_status)
    bin_node_colors = [
        [int(decision.varValue) for decision in decisions[j]] for j in range(node_count)
    ]
    solution = [color.index(1) for color in bin_node_colors]
    return solution


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    print(f"Number of nodes: {node_count}")
    print(f"Number of edges: {edge_count}")

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    if node_count**2 - (edge_count + node_count) > 0:
        solution = get_optimal_solution_1(node_count, edges)
    else:
        solution = get_optimal_solution_2(node_count, edges)

    # prepare the solution in the specified output format
    output_data = str(node_count) + " " + str(0) + "\n"
    output_data += " ".join(map(str, solution))

    return output_data


import sys

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)"
        )
