"""Safely evaluate an expression tree without Python eval or exec."""

import math

from ast_nodes import BinaryOperation, Expression, Number, UnaryOperation
from errors import EvaluationError


def evaluate(expression: Expression) -> int | float:
    """Evaluate an AST recursively, reporting division by zero explicitly."""
    if isinstance(expression, Number):
        return expression.value

    if isinstance(expression, UnaryOperation):
        value = evaluate(expression.operand)
        return value if expression.operator == "+" else -value

    left = evaluate(expression.left)
    right = evaluate(expression.right)
    if expression.operator == "+":
        result = left + right
    elif expression.operator == "-":
        result = left - right
    elif expression.operator == "*":
        result = left * right
    elif expression.operator == "/":
        if right == 0:
            raise EvaluationError(
                "Division by zero is not allowed.", position=expression.position
            )
        result = left / right
    else:
        raise EvaluationError(
            f"Unsupported operator {expression.operator!r}.",
            position=expression.position,
        )

    if isinstance(result, float) and not math.isfinite(result):
        raise EvaluationError(
            "The result is too large to represent.", position=expression.position
        )
    return result
