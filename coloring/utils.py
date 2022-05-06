from typing import Tuple
import numpy as np


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
