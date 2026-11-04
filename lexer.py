"""Tokenize arithmetic expressions into numbers and operator tokens."""

from dataclasses import dataclass
import math

from errors import LexicalError


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int


def tokenize(source: str) -> list[Token]:
    """Return all tokens in *source*, or raise a LexicalError."""
    tokens: list[Token] = []
    index = 0
    simple_tokens = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        "(": "LPAREN",
        ")": "RPAREN",
    }

    while index < len(source):
        character = source[index]
        if character.isspace():
            index += 1
            continue

        if character in simple_tokens:
            tokens.append(Token(simple_tokens[character], character, index))
            index += 1
            continue

        if character.isdigit() or character == ".":
            start = index
            has_decimal_point = False
            while index < len(source) and (
                source[index].isdigit() or source[index] == "."
            ):
                if source[index] == ".":
                    if has_decimal_point:
                        raise LexicalError(
                            f"Invalid number {source[start:index + 1]!r}: "
                            "more than one decimal point.",
                            position=index,
                        )
                    has_decimal_point = True
                index += 1

            lexeme = source[start:index]
            if lexeme == ".":
                raise LexicalError(
                    "A decimal point must be part of a number.", position=start
                )
            try:
                number = float(lexeme) if has_decimal_point else int(lexeme)
            except ValueError as error:
                raise LexicalError(
                    f"Invalid number {lexeme!r}.", position=start
                ) from error
            if isinstance(number, float) and not math.isfinite(number):
                raise LexicalError(
                    f"Number {lexeme!r} is too large to represent.",
                    position=start,
                )
            tokens.append(Token("NUMBER", lexeme, start))
            continue

        raise LexicalError(
            f"Unexpected character {character!r}. Use numbers, +, -, *, /, and parentheses.",
            position=index,
        )

    return tokens
