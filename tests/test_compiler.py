import unittest

from compiler import compile_expression
from errors import EvaluationError, LexicalError, SyntaxError
from evaluator import evaluate
from intermediate_code import generate_three_address_code
from lexer import tokenize
from parser import parse


class CompilerTests(unittest.TestCase):
    def test_lexer_recognizes_numbers_operators_and_parentheses(self) -> None:
        tokens = tokenize("(10 + 5) * 2 - 4")
        self.assertEqual(
            [token.kind for token in tokens],
            [
                "LPAREN",
                "NUMBER",
                "PLUS",
                "NUMBER",
                "RPAREN",
                "MULTIPLY",
                "NUMBER",
                "MINUS",
                "NUMBER",
            ],
        )

    def test_lexer_rejects_unknown_characters_and_malformed_numbers(self) -> None:
        with self.assertRaises(LexicalError):
            tokenize("2 @ 3")
        with self.assertRaises(LexicalError):
            tokenize("1.2.3")

    def test_parser_observes_precedence_and_parentheses(self) -> None:
        root = parse(tokenize("(10 + 5) * 2 - 4"), len("(10 + 5) * 2 - 4"))
        self.assertEqual(evaluate(root), 26)

    def test_parser_supports_unary_and_decimal_numbers(self) -> None:
        source = "-.5 + +2 * 3"
        root = parse(tokenize(source), len(source))
        self.assertEqual(evaluate(root), 5.5)

    def test_parser_rejects_trailing_unexpected_token(self) -> None:
        with self.assertRaisesRegex(SyntaxError, "Unexpected token"):
            parse(tokenize("1 2"), len("1 2"))

    def test_parser_reports_missing_parenthesis(self) -> None:
        with self.assertRaisesRegex(SyntaxError, "Missing closing parenthesis"):
            parse(tokenize("(1 + 2"), len("(1 + 2"))

    def test_parser_rejects_missing_operand(self) -> None:
        with self.assertRaises(SyntaxError):
            parse(tokenize("1 +"), len("1 +"))

    def test_three_address_code_uses_temporaries_in_postorder(self) -> None:
        source = "(10 + 5) * 2 - 4"
        root = parse(tokenize(source), len(source))
        self.assertEqual(
            generate_three_address_code(root),
            [
                "t1 = 10 + 5",
                "t2 = t1 * 2",
                "t3 = t2 - 4",
            ],
        )

    def test_evaluator_rejects_division_by_zero(self) -> None:
        source = "8 / (3 - 3)"
        root = parse(tokenize(source), len(source))
        with self.assertRaises(EvaluationError):
            evaluate(root)

    def test_complete_pipeline_returns_all_successful_outputs(self) -> None:
        result = compile_expression("(10 + 5) * 2 - 4")
        self.assertTrue(result.lexical_success)
        self.assertTrue(result.syntax_valid)
        self.assertIsNotNone(result.graphviz_source)
        self.assertEqual(len(result.instructions), 3)
        self.assertTrue(result.evaluation_success)
        self.assertEqual(result.value, 26)
        self.assertEqual(result.errors, [])

    def test_pipeline_preserves_earlier_outputs_when_evaluation_fails(self) -> None:
        result = compile_expression("8 / 0")
        self.assertTrue(result.syntax_valid)
        self.assertIsNotNone(result.graphviz_source)
        self.assertTrue(result.instructions)
        self.assertFalse(result.evaluation_success)
        self.assertIsInstance(result.errors[0], EvaluationError)

    def test_pipeline_reports_lexical_and_syntax_failures(self) -> None:
        lexical_result = compile_expression("1 @ 2")
        self.assertFalse(lexical_result.lexical_success)
        self.assertIsInstance(lexical_result.errors[0], LexicalError)

        syntax_result = compile_expression("(1 + 2")
        self.assertTrue(syntax_result.lexical_success)
        self.assertFalse(syntax_result.syntax_valid)
        self.assertIsInstance(syntax_result.errors[0], SyntaxError)


if __name__ == "__main__":
    unittest.main()
