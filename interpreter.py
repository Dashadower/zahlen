from tatsu.semantics import ModelBuilderSemantics
from .parser import ZahlenParser
from . import ast
from tatsu.walkers import NodeWalker


class ZahlenInterpreter:
    def __init__(self):
        self.pc: int = 0  # program counter
        self.label_map: dict[str, int] = {}  # maps label names to statement indices

    def read_program(self, program: str):
        pass

class ZahlenWalker(NodeWalker):
    def __init__(self):
        super().__init__()
        self.variables = {}
        self.commands = []

    def walk_Program(self, node: ast.Program):
        for statement in node.statements:
            self.walk(statement)

