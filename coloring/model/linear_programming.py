from typing import Tuple
import numpy as np
import pyomo.environ as pyo

from pyomo.core.expr.numeric_expr import SumExpression
from pyomo.opt.results.results_ import SolverResults


class LinearProgramming:
    """
    Crate linear programming model to find an optimal solution for graph coloring problem
    """

    def __init__(self, summary_edges: dict, edges: list) -> None:
        self._summary_edges = summary_edges
        self._edges = edges
        self._nodes = list(range(0, summary_edges["total_node"]))

        # initially assume that the whole possible color equal to number of node
        self._colors = list(range(0, summary_edges["total_node"]))

        self.model = self.construct_model()

    def construct_model(self) -> pyo.ConcreteModel:
        """
        Constructs pyomo concrete model object including creates variable, constraints and adding objective.
        The variable x[i] is binary variable represents whether item is selected in knapsack or not.

        Returns:
            model (pyo.ConcreteModel): concrete model object contain variables, objective and constrain.
        """
        model = LinearProgramming._init_concrete_model()
        model = LinearProgramming._adding_variables(model, self._nodes, self._colors)
        model = LinearProgramming._adding_objective_function(
            model, self._colors
        )
        model = LinearProgramming._constrain_on_adjacent_node(
            model, self._edges, self._colors
        )
        return model

    @staticmethod
    def _init_concrete_model() -> pyo.ConcreteModel:
        """
        Initiates concrete model object.

        Returns:
            model (pyo.ConcreteModel): an empty concrete model object.
        """
        model = pyo.ConcreteModel()
        model.con = pyo.ConstraintList()
        model.obj = pyo.Objective(expr=0, sense=pyo.minimize)
        return model

    @staticmethod
    def _adding_variables(
        model: pyo.ConcreteModel, nodes: list, colors: list
    ) -> pyo.ConcreteModel:
        """
        Adding variables to concrete model object.

        Args:
            model (pyo.ConcreteModel): an empty concrete model object.
            nodes (list): unique list of all node in raw data
            colors (list): unique list of number represent color

        Returns:
            model (pyo.ConcreteModel): an concrete model object with variables.
        """
        model.x = pyo.Var(nodes, colors, within=pyo.Binary)
        model.w = pyo.Var(colors, within=pyo.Binary)
        return model

    @staticmethod
    def _adding_objective_function(
        model: pyo.ConcreteModel, colors: list
    ) -> pyo.ConcreteModel:
        """
        Adding objective on minimizing number of color to concrete model object.

        Args:
            model (pyo.ConcreteModel): an empty concrete model object.
            nodes (list): unique list of all node in raw data
            colors (list): unique list of number represent color

        Returns:
            model (pyo.ConcreteModel): an concrete model object with variables.
        """
        model.obj.expr += sum(model.w[color] for color in colors)
        return model

    @staticmethod
    def _adding_constraints(
        model: pyo.ConcreteModel, edges: list, nodes: list, colors: list
    ):
        model = LinearProgramming._constrain_on_color_per_node(model, nodes, colors)
        model = LinearProgramming._constrain_on_adjacent_node(model, edges, colors)
        model = LinearProgramming._constrain_on_number_color(model, nodes, colors)
        return model

    @staticmethod
    def _constrain_on_color_per_node(
        model: pyo.ConcreteModel, nodes: list, colors: list
    ):

        for node in nodes:
            color_per_node = sum(model.x[node, color] for color in colors)
            model.con.add(expr=color_per_node == 1)
        return model

    @staticmethod
    def _constrain_on_adjacent_node(
        model: pyo.ConcreteModel, edges: list, colors: list
    ):

        for edge in edges:
            for color in colors:
                model.con.add(
                    expr=model.x[edge[0], color] + model.x[edge[1], color] <= 1
                )
        return model
    
    @staticmethod
    def _constrain_on_number_color(
        model: pyo.ConcreteModel, nodes: list, colors: list
    ):

        for node in nodes:
            for color in colors:
                model.con.add(expr=model.x[node, color] <= model.w[color])
        return model

    @staticmethod
    def solve(
        model: pyo.ConcreteModel, solver: str = "glpk"
    ) -> Tuple[SolverResults, dict]:
        """
        Activate optimization process.

        Args:
            model (pyo.ConcreteModel): concrete model object contain variables, objective and constrain.
            solver (str): name of solver that will be used in optimization process.

        Returns:
            solver_result (SolverResults): pyomo object contains summary of solver log
            optimized_solution (dict): dictionary contain solved variable x
        """
        opt = pyo.SolverFactory(solver)
        solver_result = opt.solve(model, tee=True)
        optimized_solution = model.x.get_values()
        return solver_result, optimized_solution
