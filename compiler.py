"""Run the compiler phases and collect their outputs for the interface."""

from dataclasses import dataclass, field

from ast_nodes import Expression, to_graphviz
from errors import CompilerError
from evaluator import evaluate
from intermediate_code import generate_three_address_code
from lexer import Token, tokenize
from parser import parse


@dataclass
class CompilationResult:
    tokens: list[Token] = field(default_factory=list)
    syntax_valid: bool = False
    expression_tree: Expression | None = None
    graphviz_source: str | None = None
    instructions: list[str] = field(default_factory=list)
    value: int | float | None = None
    errors: list[CompilerError] = field(default_factory=list)
    lexical_success: bool = False
    evaluation_success: bool = False


def compile_expression(source: str) -> CompilationResult:
    """Run lexical analysis, parsing, code generation, and evaluation."""
    result = CompilationResult()

    try:
        result.tokens = tokenize(source)
        result.lexical_success = True
    except CompilerError as error:
        result.errors.append(error)
        return result

    try:
        result.expression_tree = parse(result.tokens, len(source))
        result.syntax_valid = True
    except CompilerError as error:
        result.errors.append(error)
        return result

    result.graphviz_source = to_graphviz(result.expression_tree).source
    result.instructions = generate_three_address_code(result.expression_tree)
    try:
        result.value = evaluate(result.expression_tree)
        result.evaluation_success = True
    except CompilerError as error:
        result.errors.append(error)

    return result
