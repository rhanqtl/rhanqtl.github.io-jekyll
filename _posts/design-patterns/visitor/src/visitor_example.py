#!/usr/bin/env python3

from __future__ import annotations
import abc
from typing import Union

#
# Expr's
#
class Expr(abc.ABC):
    def accept(self, v: Visitor): pass

class Literal(Expr):
    def __init__(self, value: Union[int, float, bool]):
        self.value = value

    def accept(self, v: Visitor):
        return v.visit_literal(self)

class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def accept(self, v: Visitor):
        return v.visit_variable(self)

class UnaryExpr(Expr):
    def __init__(self, op: str, x: Expr):
        self.op = op
        self.x = x

    def accept(self, v: Visitor):
        return v.visit_unary_expr(self)

class BinaryExpr(Expr):
    def __init__(self, op: str, lhs: Expr, rhs: Expr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def accept(self, v: Visitor):
        return v.visit_binary_expr(self)

#
# Visitor's
#
class Visitor(abc.ABC):
    def visit_literal(self, n: Literal): pass
    def visit_variable(self, v: Variable): pass
    def visit_unary_expr(self, expr: UnaryExpr): pass
    def visit_binary_expr(self, expr: BinaryExpr): pass

class RPNVisitor(Visitor):
    def visit_literal(self, n: Literal):
        return str(n.value)

    def visit_variable(self, v: Variable):
        return str(v.name)

    def visit_unary_expr(self, expr: UnaryExpr):
        return "{} {}".format(expr.x.accept(self), expr.op)

    def visit_binary_expr(self, expr: BinaryExpr):
        return "{} {} {}".format(expr.lhs.accept(self), expr.rhs.accept(self), expr.op)

class CanonVisitor(Visitor):
    def visit_literal(self, n: Literal):
        return str(n.value)

    def visit_variable(self, v: Variable):
        return str(v.name)

    def visit_unary_expr(self, expr: UnaryExpr):
        return "({} {})".format(expr.op, expr.x.accept(self))

    def visit_binary_expr(self, expr: BinaryExpr):
        return "({} {} {})".format(expr.lhs.accept(self), expr.op, expr.rhs.accept(self))

class EvalVisitor(Visitor):
    def visit_literal(self, n: Literal):
        return n.value

    def visit_variable(self, v: Variable):
        raise Exception("not supported yet")

    def visit_unary_expr(self, expr: UnaryExpr):
        match expr.op:
            case "-": return -expr.x.accept(self)
            case "not": return not expr.x.accept(self)
            case _: raise Exception("unsupported unary operator: {}".format(expr.op))

    def visit_binary_expr(self, expr: BinaryExpr):
        match expr.op:
            case "+":   return expr.lhs.accept(self) + expr.rhs.accept(self)
            case "-":   return expr.lhs.accept(self) - expr.rhs.accept(self)
            case "*":   return expr.lhs.accept(self) * expr.rhs.accept(self)
            case "/":   return expr.lhs.accept(self) / expr.rhs.accept(self)
            case "and": return expr.lhs.accept(self) and expr.rhs.accept(self)
            case "or":  return expr.lhs.accept(self) or expr.rhs.accept(self)
            case _:     raise Exception("unsupported binary operator: {}".format(expr.op))


if __name__ == "__main__":
    expr = \
        BinaryExpr(
            "AND",
            BinaryExpr(
                "OR",
                BinaryExpr(
                    ">",
                    Variable("a"),
                    Literal(0),
                ),
                BinaryExpr(
                    "!=",
                    Variable("b"),
                    Literal(1),
                ),
            ),
            UnaryExpr(
                "NOT",
                Variable("c"),
            ),
        )

    # print(expr.accept(RPNVisitor()))
    # print(expr.accept(CanonVisitor()))

    expr = \
        BinaryExpr(
            "+",
            BinaryExpr(
                "+",
                Literal(1),
                BinaryExpr(
                    "*",
                    Literal(2),
                    Literal(3),
                ),
            ),
            Literal(4),
        )

    print(expr.accept(CanonVisitor()))
    print(expr.accept(EvalVisitor()))
