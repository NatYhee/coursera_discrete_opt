#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import format_input, get_edges_connection_array
from model.linear_programming import LinearProgramming


def solve_it(input_data):
    """
    Solving coloring problem with linear programming from given input_data.

    Args:
        input_data (str): input data of node and edges for coloring.

    Returns:
        output_data (str): output data of itemse selected in knapsack.
    """

    # parse the input
    edges, summary_edges = format_input(input_data)
    connection_array = get_edges_connection_array(edges, summary_edges)

    # preparing for linear programming to solve the issue
    lp_optimizer = LinearProgramming(summary_edges, connection_array, edges)

    # build a trivial solution
    # every node has its own color
    solution = range(0, summary_edges["total_node"])

    # prepare the solution in the specified output format
    output_data = str(summary_edges["total_node"]) + " " + str(0) + "\n"
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
