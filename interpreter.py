from parser import ZahlenParser
import zahlen_ast as zast
from tatsu.semantics import ModelBuilderSemantics
from typing import Union, Type, Callable
from numbers import Number
from dataclasses import dataclass
from basewalker import ZahlenWalker, ZahlenExpressionValueExecutor
import time


class ZahlenInterpreter:
    def __init__(self):
        self.pc: int = 0  # program counter
        self.label_map: dict[str, int] = {}  # maps label names to statement indices
        self.statements = []  # list of the statement ASTs in order. Its indices become the program counter

        self.variable_values: dict[str, int] = {}  # maps variable names to values
        self.parser = ZahlenParser()

    def read_program(self, program: str):
        self.label_map = {}
        self.statements = []
        ast = self.parser.parse(program, semantics=ModelBuilderSemantics(), trace=False)
        for index, statement in enumerate(ast.statements):
            walker = ZahlenStatementWalker()
            walker.walk(statement)
            self.statements.append(walker.statement_ast)
            if walker.label:
                self.label_map[walker.label] = index

    def run_program(self) -> None:
        self.pc = 0
        self.variable_values = {}
        n_statements = len(self.statements)

        executor = ZahlenExecutorWalker(get_variable_func=self.get_variable_value,
                                        set_variable_func=self.set_variable_value,
                                        increment_pc_func=self.increment_pc,
                                        set_pc_label_func=self.set_pc_from_label)

        while self.pc < n_statements:
            #print(f"PC: {self.pc}")
            current_statement = self.statements[self.pc]
            executor.walk(current_statement)

        print(f"FINISHED EXECUTION. final variable values:")
        print(self.variable_values)

    def print_ast(self) -> None:
        for stmt in self.statements:
            print(stmt)

    def get_variable_value(self, varname: str):
        return self.variable_values[varname]

    def set_variable_value(self, varname: str, value: int):
        assert isinstance(value, int) or isinstance(value, list), f"Value to write to variable {varname} isnt a integer type; has value {value}"
        self.variable_values[varname] = value

    def increment_pc(self):
        self.pc += 1

    def set_pc_from_label(self, label: str):
        self.pc = self.label_map[label]


class ZahlenExecutorWalker(ZahlenExpressionValueExecutor):
    def __init__(self, get_variable_func: Callable, set_variable_func: Callable,
                 increment_pc_func: Callable, set_pc_label_func: Callable):
        super().__init__()
        self.get_variable_func = get_variable_func
        self.set_variable_func = set_variable_func
        self.increment_pc_func = increment_pc_func
        self.set_pc_label_func = set_pc_label_func

    def walk_Assignment(self, node: zast.Assignment):
        variable_name = node.varname.varname
        rhs_value = self.walk(node.rhs)
        self.set_variable_func(variable_name, rhs_value)
        self.increment_pc_func()

    def walk_Skip(self, node: zast.Skip):
        self.increment_pc_func()

    def walk_GoTo(self, node: zast.GoTo):
        label = node.label
        self.set_pc_label_func(label)

    def walk_IfElse(self, node: zast.IfElse):
        if self.walk(node.pred):
            self.walk(node.true_stmt)
        else:
            self.walk(node.false_stmt)

    def walk_Print(self, node: zast.Print):
        value = self.walk(node.expression)
        print(value)
        self.increment_pc_func()

    def walk_Variable(self, node: zast.Variable):
        varname = node.varname
        return self.get_variable_func(varname)

    def walk_Array(self, node: zast.Array):
        value = [self.walk(element) for element in node.elements]
        return value

    def walk_ArrayIndex(self, node: zast.ArrayIndex):
        varname = node.varname
        # Currently only supports 1d arrays
        return self.walk(varname)[self.walk(node.index)]


@dataclass
class ZahlenStatementWalker(ZahlenWalker):
    label: str = ""
    statement_ast: zast.ModelBase = None

    def walk_LabeledStatement(self, node: zast.LabeledStatement):
        self.label = node.label
        self.statement_ast = node.statement

    def walk_Print(self, node: zast.Print):
        self.statement_ast = node

    def walk_Skip(self, node: zast.Skip):
        self.statement_ast = node

    def walk_Assignment(self, node: zast.Assignment):
        self.statement_ast = node

    def walk_IfElse(self, node: zast.IfElse):
        self.statement_ast = node

    def walk_GoTo(self, node: zast.GoTo):
        self.statement_ast = node

if __name__ == '__main__':
    i = ZahlenInterpreter()
    i.read_program(open("zahlen_sources/array_decl.z").read())
    i.print_ast()
    i.run_program()
