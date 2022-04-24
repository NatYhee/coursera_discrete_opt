from collections import namedtuple
from typing import Tuple
from pyomo.opt.results.results_ import SolverResults

Item = namedtuple("Item", ["index", "value", "weight"])


def format_input(input_data: str) -> Tuple[namedtuple, dict]:
    """
    Transform input_data into desired format before putting in optimizer.

    Args:
        input_data (str): string of input data extracted from the raw file.

    Returns:
        items (namedtuple): named tuple contain information of each item.
        summary_items (dict): dictionary contains summary information of input.
    """

    lines = input_data.split("\n")

    # extract information from first row
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    summary_items = {"total_items": item_count, "total_capacity": capacity}

    # extract information from after conclusion row
    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    return items, summary_items


def get_opt_ending_status(solver_summary: SolverResults) -> str:
    """
    Extracting termination condition from SolverResults object which is log of solver status.

    Args:
        solver_summary (SolverResults): object that contains log of solver status.

    Returns:
        termination_condition (str): status flag whether solver ends up with optimal result of not.
    """
    solver_status = solver_summary.Solver._list
    termination_condition = str(solver_status[0]["termination_condition"])
    return termination_condition


def format_output(knapsack_dict: dict, solver_summary: SolverResults) -> str:
    """
    Preparing final output data.

    Args:
        solver_summary (SolverResults): object that contains log of solver status.

    Returns:
        termination_condition (str): status flag whether solver ends up with optimal result of not.
    """
    termination_condition = get_opt_ending_status(solver_summary)

    optimal = 1 if termination_condition == "optimal" else 0
    output_data = str(knapsack_dict["value"]) + " " + str(optimal) + "\n"
    output_data += " ".join(map(str, knapsack_dict["selected_items"]))

    return output_data
