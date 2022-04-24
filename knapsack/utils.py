from collections import namedtuple

Item = namedtuple("Item", ["index", "value", "weight"])


def format_input(input_data: str):
    """
    Transform input_data into desired format before putting in optimizer.

    Args:
        input_data (str): string of input data extracted from the raw file

    Returns:
        items (Item): named tuple contain information of each item
        summary_items (dict): dictionary contains summary information of input
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


def get_opt_ending_status(solver_summary):
    solver_status = solver_summary.Solver._list
    termination_condition = str(solver_status[0]["termination_condition"])
    return termination_condition


def format_output(knapsack_dict, solver_summary):
    termination_condition = get_opt_ending_status(solver_summary)

    optimal = 1 if termination_condition == "optimal" else 0
    output_data = str(knapsack_dict["value"]) + " " + str(optimal) + "\n"
    output_data += " ".join(map(str, knapsack_dict["selected_items"]))

    return output_data
