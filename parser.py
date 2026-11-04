"""Recursive descent parser for the project's arithmetic grammar."""

from ast_nodes import BinaryOperation, Expression, Number, UnaryOperation
from errors import SyntaxError
from lexer import Token


GRAMMAR = """\
expression  -> term ((\"+\" | \"-\") term)*
term        -> unary ((\"*\" | \"/\") unary)*
unary       -> (\"+\" | \"-\") unary | primary
primary     -> NUMBER | \"(\" expression \")\"\
"""


class Parser:
    """Parse a token sequence using precedence-aware recursive descent."""

    def __init__(self, tokens: list[Token], source_length: int) -> None:
        self.tokens = tokens
        self.source_length = source_length
        self.index = 0

    def parse(self) -> Expression:
        if not self.tokens:
            raise SyntaxError("Expression is empty.", position=0)

        expression = self._expression()
        if self._current() is not None:
            token = self._current()
            assert token is not None
            raise SyntaxError(
                f"Unexpected token {token.value!r} after a complete expression.",
                position=token.position,
            )
        return expression

    def _expression(self) -> Expression:
        node = self._term()
        while (token := self._current()) is not None and token.kind in {
            "PLUS",
            "MINUS",
        }:
            self.index += 1
            right = self._term()
            node = BinaryOperation(token.value, node, right, token.position)
        return node

    def _term(self) -> Expression:
        node = self._unary()
        while (token := self._current()) is not None and token.kind in {
            "MULTIPLY",
            "DIVIDE",
        }:
            self.index += 1
            right = self._unary()
            node = BinaryOperation(token.value, node, right, token.position)
        return node

    def _unary(self) -> Expression:
        token = self._current()
        if token is not None and token.kind in {"PLUS", "MINUS"}:
            self.index += 1
            return UnaryOperation(token.value, self._unary(), token.position)
        return self._primary()

    def _primary(self) -> Expression:
        token = self._current()
        if token is None:
            raise SyntaxError(
                "Unexpected end of input; expected a number or '('.",
                position=self.source_length,
            )

        if token.kind == "NUMBER":
            self.index += 1
            value = float(token.value) if "." in token.value else int(token.value)
            return Number(value, token.value, token.position)

        if token.kind == "LPAREN":
            self.index += 1
            if (next_token := self._current()) is not None and next_token.kind == "RPAREN":
                raise SyntaxError(
                    "Expected an expression inside the parentheses.",
                    position=next_token.position,
                )
            expression = self._expression()
            if (closing := self._current()) is None or closing.kind != "RPAREN":
                raise SyntaxError(
                    "Missing closing parenthesis ')'.",
                    position=(
                        closing.position
                        if closing is not None
                        else self.source_length
                    ),
                )
            self.index += 1
            return expression

        raise SyntaxError(
            f"Expected a number or '('; got {token.value!r}.",
            position=token.position,
        )

    def _current(self) -> Token | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]


def parse(tokens: list[Token], source_length: int) -> Expression:
    """Parse *tokens* and return the root expression node."""
    return Parser(tokens, source_length).parse()
