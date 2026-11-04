"""Generate three-address code from the abstract syntax tree."""

from ast_nodes import BinaryOperation, Expression, Number, UnaryOperation


def generate_three_address_code(expression: Expression) -> list[str]:
    """Return one temporary assignment for each AST operation."""
    instructions: list[str] = []
    temporary_index = 0

    def generate(node: Expression) -> str:
        nonlocal temporary_index
        if isinstance(node, Number):
            return node.lexeme

        if isinstance(node, UnaryOperation):
            operand = generate(node.operand)
            temporary_index += 1
            temporary = f"t{temporary_index}"
            instructions.append(f"{temporary} = {node.operator}{operand}")
            return temporary

        left = generate(node.left)
        right = generate(node.right)
        temporary_index += 1
        temporary = f"t{temporary_index}"
        instructions.append(
            f"{temporary} = {left} {node.operator} {right}"
        )
        return temporary

    generate(expression)
    return instructions
