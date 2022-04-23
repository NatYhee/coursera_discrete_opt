#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import format_input
from model.optimizer import LinearOptimizer

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    items, summary_items = format_input(input_data)

    optimizer = LinearOptimizer(items, summary_items)
    result = optimizer._solve(optimizer.model)
    breakpoint()
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

