from typing import Tuple
import numpy as np
from pyomo.opt.results.results_ import SolverResults


def format_input(input_data: str) -> Tuple[list, dict]:
    """
    Transform input_data into desired format before putting in optimizer.

    Args:
        input_data (str): string of input data extracted from the raw file.

    Returns:
        edges (list): list of tuple contains information of source node, first index of tuple, and target node, second element of tuple.
        summary_dict (dict): dictionary contains summary information of number of node and number of edges.
    """

    lines = input_data.split("\n")

    # extract information from first row
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    summary_dict = {"total_node": node_count, "total_edge": edge_count}

    # extract information from after conclusion row
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    return edges, summary_dict


def get_edges_connection_array(edges: list, summary_edges: dict) -> np.ndarray:
    """
    Create metrix size total_node*total_node which represent the conection between node[i], row, to node[j], column.

    Args:
        edges (list): list of tuple contains information of source node, first index of tuple, and target node, second element of tuple.
        summary_edges (dict): dictionary contains summary information of number of node and number of edges.

    Returns:
        edges_connection_array (np.ndarray): two dimension binary array which row represent source node and column represent destination node.
    """
    total_node = summary_edges["total_node"]
    edges_connection_array = np.zeros((total_node, total_node))

    for edge in edges:
        edges_connection_array[edge[0]][edge[1]] = int(1)

    return edges_connection_array


def reformat_solution(solver_solution: dict) -> list:
    """
    Reformat solution from solver to prepare for output table

    Args:
        solver_solution (dict): dictionary contain value of decision variable.

    Returns:
        solution (list): list of color of each node. The list index represents node and the value of index represents color.
    """

    post_process_solution = []

    for node_color in solver_solution.keys():
        if solver_solution[node_color] == 1:
            post_process_solution.append(node_color[1])

    return post_process_solution


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


def format_output(solution: list, solver_summary: SolverResults) -> str:
    """
    Preparing final output data.

    Args:
        solution (list): list of color of each node. The list index represents node and the value of index represents color.
        solver_summary (SolverResults): object that contains log of solver status.

    Returns:
        output_data (str): final output in determined format.
    """
    termination_condition = get_opt_ending_status(solver_summary)
    optimal = 1 if termination_condition == "optimal" else 0

    total_color = len(set(solution))

    output_data = str(total_color) + " " + str(optimal) + "\n"
    output_data += " ".join(map(str, solution))
    return output_data
