"""Compiler diagnostics shared by the lexer, parser, and evaluator."""


class CompilerError(Exception):
    """An expected, user-facing compiler error."""

    def __init__(
        self, message: str, *, phase: str, position: int | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.phase = phase
        self.position = position

    def __str__(self) -> str:
        if self.position is None:
            return self.message
        return f"{self.message} (at character {self.position + 1})"


class LexicalError(CompilerError):
    def __init__(self, message: str, *, position: int | None = None) -> None:
        super().__init__(message, phase="Lexical analysis", position=position)


class SyntaxError(CompilerError):
    def __init__(self, message: str, *, position: int | None = None) -> None:
        super().__init__(message, phase="Syntax analysis", position=position)


class EvaluationError(CompilerError):
    def __init__(self, message: str, *, position: int | None = None) -> None:
        super().__init__(message, phase="Expression evaluation", position=position)
