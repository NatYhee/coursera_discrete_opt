#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import format_input, format_output
from model.optimizer import LinearOptimizer


def solve_it(input_data: str) -> str:
    """
    Solving knapsack problem for given input_data.

    Args:
        input_data (str): input data of items for selection in knapsack.

    Returns:
        output_data (str): output data of itemse selected in knapsack.
    """
    # Modify this code to run your optimization algorithm
    items, summary_items = format_input(input_data)

    optimizer = LinearOptimizer(items, summary_items)
    solver_summary, optimized_solution = optimizer._solve(optimizer.model)

    ls_knapsack = [int(value) for value in optimized_solution.values()]
    ls_knapsack_value = [
        items[i].value if ls_knapsack[i] == 1 else 0 for i in range(len(ls_knapsack))
    ]
    ls_knapsack_weight = [
        items[i].weight if ls_knapsack[i] == 1 else 0 for i in range(len(ls_knapsack))
    ]

    knapsack_dict = {
        "selected_items": ls_knapsack,
        "value": sum(ls_knapsack_value),
        "weight": sum(ls_knapsack_weight),
    }

    # prepare the solution in the specified output format
    output_data = format_output(knapsack_dict, solver_summary)
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
