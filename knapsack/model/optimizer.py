from collections import namedtuple
from typing import Dict
from prometheus_client import Summary
import pyomo.environ as pyo

from pyomo.core.expr.numeric_expr import SumExpression
from pyomo.opt.results.results_ import SolverResults


class LinearOptimizer:
    def __init__(self, items: namedtuple, summary_items: dict) -> None:
        self.items = items
        self.summary_items = summary_items
        self.model = self.construct_model()

    def construct_model(self):
        model = LinearOptimizer.init_concrete_model()
        model = LinearOptimizer._adding_variables(model, self.summary_items)

        total_value = sum(
            model.x[i] * self.items[i].value
            for i in range(self.summary_items["total_items"])
        )
        model.obj.expr += total_value

        used_capacity = sum(
            model.x[i] * self.items[i].weight
            for i in range(self.summary_items["total_items"])
        )
        model.con.add(expr=used_capacity <= self.summary_items["total_capacity"])
        return model

    @staticmethod
    def init_concrete_model():
        model = pyo.ConcreteModel()
        model.con = pyo.ConstraintList()
        model.obj = pyo.Objective(expr=0, sense=pyo.maximize)
        return model

    @staticmethod
    def _adding_variables(model: pyo.ConcreteModel, summary_items: dict):
        model.x = pyo.Var(range(summary_items["total_items"]), within=pyo.Binary)
        model.w = pyo.Var(
            range(summary_items["total_items"]), within=pyo.NonNegativeIntegers
        )
        return model

    @staticmethod
    def _solve(model: pyo.ConcreteModel, solver: str = "glpk"):
        opt = pyo.SolverFactory(solver)
        solver_result = opt.solve(model, tee=True)
        optimized_solution = model.x.get_values()
        return solver_result, optimized_solution
