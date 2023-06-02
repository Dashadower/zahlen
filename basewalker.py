import zahlen_ast as zast
from tatsu.walkers import NodeWalker


class ZahlenWalker(NodeWalker):
    def __init__(self):
        super().__init__()

    def walk_Program(self, node: zast.Program):
        raise NotImplementedError

    def walk_BinaryIntExpr(self, node: zast.BinaryIntExpr):
        raise NotImplementedError

    def walk_BinaryBoolExpr(self, node: zast.BinaryBoolExpr):
        raise NotImplementedError

    def walk_Boolean(self, node: zast.Boolean):
        raise NotImplementedError

    def walk_LabeledStatement(self, node: zast.LabeledStatement):
        raise NotImplementedError

    def walk_Assignment(self, node: zast.Assignment):
        raise NotImplementedError

    def walk_Skip(self, node: zast.Skip):
        raise NotImplementedError

    def walk_IfElse(self, node: zast.IfElse):
        raise NotImplementedError

    def walk_GoTo(self, node: zast.GoTo):
        raise NotImplementedError

    def walk_Print(self, node: zast.Print):
        raise NotImplementedError

    def walk_Integer(self, node: zast.Integer):
        raise NotImplementedError

    def walk_Variable(self, node: zast.Variable):
        raise NotImplementedError


class ZahlenExpressionValueExecutor(ZahlenWalker):
    def walk_BinaryIntExpr(self, node: zast.BinaryIntExpr) -> int:
        left_value = self.walk(node.left)
        right_value = self.walk(node.right)

        match node.op:
            case "+":
                return left_value + right_value
            case "-":
                return left_value - right_value
            case "*":
                return left_value * right_value
            case "/":
                return left_value / right_value

    def walk_BinaryBoolExpr(self, node: zast.BinaryIntExpr) -> bool:
        left_value = self.walk(node.left)
        right_value = self.walk(node.right)

        match node.op:
            case "==":
                return left_value == right_value
            case "!=":
                return left_value != right_value
            case ">=":
                return left_value >= right_value
            case "<=":
                return left_value < right_value
            case ">":
                return left_value > right_value
            case "<":
                return left_value < right_value
            case "||":
                return left_value or right_value
            case "&&":
                return left_value and right_value

    def walk_Boolean(self, node: zast.Boolean) -> bool:
        if node.value == "true":
            print("reached bool true")
            return True
        elif node.value == "false":
            return False

    def walk_Integer(self, node: zast.Integer):
        return int(node.value)
