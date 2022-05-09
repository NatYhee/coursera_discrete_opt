import numpy as np
import pyomo.environ as pyo

from pyomo.core.expr.numeric_expr import SumExpression
from pyomo.opt.results.results_ import SolverResults

class LinearProgramming:
    """
    Crate linear programming model to find an optimal solution for graph coloring problem
    """

    def __init__(self, summary_edges:dict, connection_array:np.ndarray, edges_data:list) -> None:
        self._summary_edges = summary_edges
        self._connection_array = connection_array
        self._edges_data = edges_data
    
    def construct_model(self) -> pyo.ConcreteModel:
        """
        Constructs pyomo concrete model object including creates variable, constraints and adding objective.
        The variable x[i] is binary variable represents whether item is selected in knapsack or not.

        Returns:
            model (pyo.ConcreteModel): concrete model object contain variables, objective and constrain.
        """
        model = LinearProgramming._init_concrete_model()
        model = LinearProgramming._adding_variables(model, self._summary_edges, self._edges_data)

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
        model: pyo.ConcreteModel, summary_edges: dict, edges_data:list
    ) -> pyo.ConcreteModel:
        """
        Adding variables to concrete model object.

        Args:
            model (pyo.ConcreteModel): an empty concrete model object.
            summary_edges (dict): a dictionary contains summary of edges data.
            edges_data (list): rew data of node and connection

        Returns:
            model (pyo.ConcreteModel): an concrete model object with variables.
        """
        color = range(summary_edges["total_nodes"])
        node = list(set([edges[0] for edges in edges_data]))

        model.x = pyo.Var(
            node, color, within=pyo.Binary
        )
        return model
