from typing import Tuple


def format_input(input_data: str) -> Tuple[list, dict]:
    """
    Transform input_data into desired format before putting in optimizer.

    Args:
        input_data (str): string of input data extracted from the raw file.

    Returns:
        edges (namedtuple): named tuple with two elements which its first element is source node and the second element is target node.
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


def get_edges_connection_array(edges: list):
    pass
