#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import (
    format_input,
    get_edges_connection_array,
    reformat_solution,
    format_output,
)
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

    # preparing for linear programming to solve the issue
    lp_optimizer = LinearProgramming(summary_edges, edges)
    solver_summary, optimized_solution = lp_optimizer.solve(lp_optimizer.model)

    # preparing for output file
    post_process_solution = reformat_solution(optimized_solution)
    output_data = format_output(post_process_solution, solver_summary)

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
