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
        ast = self.parser.parse(program, semantics=ModelBuilderSemantics(), trace=False, parseinfo=False)
        for index, statement in enumerate(ast.statements):
            self.statements.append(statement)

    def run_program(self) -> None:
        self.pc = 0
        self.variable_values = {}
        n_statements = len(self.statements)

        executor = ZahlenExecutorWalker(get_variable_func=self.get_variable_value,
                                        set_variable_func=self.set_variable_value,
                                        increment_pc_func=self.increment_pc,
                                        set_pc_func=self.set_pc_explicit,
                                        get_pc_func=self.get_current_pc)

        while self.pc < n_statements:
            #print(f"PC: {self.pc}")
            current_statement = self.statements[self.pc]
            executor.walk(current_statement)

        print(f"Finished interpretation. Final variable values:")
        print(self.variable_values)

    def print_ast(self) -> None:
        for stmt in self.statements:
            print(stmt)

    def get_variable_value(self, varname: str):
        return self.variable_values[varname]

    def set_variable_value(self, varname: str, value: int):
        assert isinstance(value, int) or isinstance(value, list), f"Value to write to variable {varname} isnt a integer type; has value {value}"
        self.variable_values[varname] = value

    def get_current_pc(self) -> int:
        return self.pc

    def increment_pc(self):
        self.pc += 1

    def set_pc_explicit(self, value: int):
        self.pc = value


class ZahlenExecutorWalker(ZahlenExpressionValueExecutor):
    def __init__(self, get_variable_func: Callable, set_variable_func: Callable,
                 increment_pc_func: Callable, set_pc_func: Callable, get_pc_func: Callable):
        super().__init__()
        self.get_variable_func = get_variable_func
        self.set_variable_func = set_variable_func
        self.increment_pc_func = increment_pc_func
        self.set_pc_func = set_pc_func
        self.get_pc_func = get_pc_func

    def walk_Assignment(self, node: zast.Assignment):
        variable_name = node.varname.varname
        rhs_value = self.walk(node.rhs)
        self.set_variable_func(variable_name, rhs_value)
        self.increment_pc_func()

    def walk_Skip(self, node: zast.Skip):
        self.increment_pc_func()

    def walk_IfElse(self, node: zast.IfElse):
        if self.walk(node.pred):
            self.walk(node.true_statement)
        else:
            self.walk(node.false_statement)

    def walk_Print(self, node: zast.Print):
        value = self.walk(node.expression)
        print(value)
        self.increment_pc_func()

    def walk_While(self, node: zast.While):
        entry_pc = self.get_pc_func()  # This is the PC of the while statement
        pred_value = self.walk(node.pred)
        if pred_value:
            for stmt in node.statements:  # Note that inner statements don't get PC values. But they modify it
                self.walk(stmt)

            self.set_pc_func(entry_pc)  # Since we don't want to keep the wrongly modified PC, reset it
        else:
            self.set_pc_func(entry_pc)
            self.increment_pc_func()  # If the while loop is finished, we advance to the next statement

    def walk_Variable(self, node: zast.Variable):
        varname = node.varname
        return self.get_variable_func(varname)

    def walk_Array(self, node: zast.Array):
        value = [self.walk(element) for element in node.elements]
        return value

    def walk_ArrayIndex(self, node: zast.ArrayIndex):
        varname = node.varname
        return self.walk(varname)[self.walk(node.index)]


if __name__ == '__main__':
    i = ZahlenInterpreter()
    i.read_program(open("zahlen_sources/fibonacci.z").read())
    #i.print_ast()
    i.run_program()
