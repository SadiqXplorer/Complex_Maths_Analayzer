# MathX – Mathematical Expression Compiler & Analyzer

MathX is a small, beginner-friendly B.Tech Compiler Design project. It accepts
arithmetic expressions and shows how a compiler can turn source text into
tokens, validate its structure, build a syntax tree, generate intermediate
code, detect errors, and calculate a result.

The project is intentionally limited to those six compiler features. It has no
accounts, database, network service, or use of Python's `eval()` or `exec()`.

## Objectives

- Understand the main stages in a simple compiler.
- Implement a custom tokenizer and recursive descent parser.
- See operator precedence represented as a tree.
- Generate readable three-address code (3AC).
- Report lexical, syntax, and division-by-zero errors.
- Safely calculate an expression by walking its syntax tree.

## What is a compiler?

A compiler translates a program from one representation to another. A
traditional compiler may translate a high-level language into machine code.
MathX is a mini compiler: it translates a mathematical expression into tokens,
a tree, and intermediate code, and then evaluates that tree. Its stages make
the translation steps visible rather than hiding them in a library.

## Implemented compiler phases

### 1. Lexical analysis

The custom lexer reads the input from left to right and groups characters into
tokens. The supported token kinds are:

| Token kind | Example |
|---|---|
| `NUMBER` | `12`, `3.5`, `.25` |
| `PLUS`, `MINUS` | `+`, `-` |
| `MULTIPLY`, `DIVIDE` | `*`, `/` |
| `LPAREN`, `RPAREN` | `(`, `)` |

Whitespace is ignored. Every token keeps its source position, which helps
explain where an error occurred. Unknown characters and malformed numbers are
reported as lexical errors.

### 2. Syntax analysis

The parser checks whether the token sequence follows the arithmetic grammar.
It is a hand-written **Recursive Descent Parser**: each grammar rule has a
corresponding parser method, and a method can call another method to parse a
smaller part of the expression.

The grammar (CFG) is:

```text
expression -> term (("+" | "-") term)*
term       -> unary (("*" | "/") unary)*
unary      -> ("+" | "-") unary | primary
primary    -> NUMBER | "(" expression ")"
```

The grammar is context-free because each production replaces one
non-terminal with a sequence of terminals and/or non-terminals. Splitting
`expression`, `term`, and `unary` gives multiplication and division higher
precedence than addition and subtraction. Parentheses are parsed as a complete
expression. Unary signs such as `-4` are supported; exponentiation and implicit
multiplication (such as `2(3+4)`) are not.

### 3. Parse tree

When parsing succeeds, MathX creates an abstract syntax tree (AST). Number
nodes are leaves; operator nodes hold their operand or left and right
subexpressions. For `(2 + 3) * 4`, the root is `*`, with `+` as its left child
and `4` as its right child. The interface renders this AST with Graphviz.

### 4. Three-address code

Three-address code stores each operation in a temporary. This makes the
evaluation order explicit and keeps each instruction simple.

For `(10 + 5) * 2 - 4`, MathX generates:

```text
t1 = 10 + 5
t2 = t1 * 2
t3 = t2 - 4
```

The instructions are emitted in postorder: the operands of an operation are
generated before that operation. A single-number expression has no operation
to place in 3AC.

### 5. Error detection

MathX identifies:

- **Invalid characters or numbers** during lexical analysis, for example
  `2 @ 3` or `1.2.3`.
- **Invalid syntax or unexpected tokens**, for example `1 + * 2` or `1 2`.
- **Missing parentheses**, for example `(1 + 2`.
- **Division by zero** during evaluation, including a denominator that
  evaluates to zero, for example `8 / (3 - 3)`.

Once a phase fails, later phases that depend on it do not run. If only
evaluation fails, the valid tokens, syntax tree, and 3AC remain available.
Diagnostics include a character position when one is known.

### 6. Expression evaluation

The evaluator recursively walks the validated AST. It applies the operator at
each node to the values of its children. It does not interpret the source as
Python and never calls `eval()` or `exec()`. Division by zero and results that
cannot be represented as finite numbers are reported instead of hidden.

## Architecture

```text
Input expression
      |
    lexer.py  ----> tokens
      |
    parser.py ----> AST (ast_nodes.py) ----> Graphviz tree
                              |
                intermediate_code.py ----> 3AC
                              |
                     evaluator.py -------> result
      |
    errors.py: shared compiler diagnostics
    compiler.py: runs phases and collects their outputs
    app.py: Streamlit interface
```

| File | Responsibility |
|---|---|
| `app.py` | Dark glass-style Streamlit UI and compiler output views |
| `lexer.py` | Token definitions and custom lexical analysis |
| `parser.py` | CFG and recursive descent parser |
| `ast_nodes.py` | AST node types and Graphviz representation |
| `intermediate_code.py` | Three-address code generation |
| `evaluator.py` | Safe recursive arithmetic evaluation |
| `errors.py` | Clear errors shared between compiler phases |
| `compiler.py` | Runs the phases and gathers their outputs |
| `tests/test_compiler.py` | Automated tests for the six required features |
| `requirements.txt` | Python package requirements |

## Installation and execution

Use Python 3.11 or newer. Graphviz is rendered by Streamlit's Graphviz chart
component; the Python Graphviz package is included as a project dependency.

```bash
python -m venv .venv
```

Activate it, then install dependencies and start the application:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

```bash
# macOS / Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Enter an expression and choose
**Compile expression**. Use **Clear** to reset the editor and output.

Run the automated tests from the project directory:

```bash
python -m unittest discover -s tests -v
```

## Sample test cases

| Expression | Expected behavior |
|---|---|
| `(10 + 5) * 2 - 4` | Valid; result `26`; three 3AC instructions |
| `8 / (3 - 3)` | Valid syntax; division-by-zero error at evaluation |
| `1 + * 2` | Syntax error: an operand was expected |
| `(1 + 2` | Syntax error: missing closing parenthesis |
| `1 2` | Syntax error: unexpected trailing number |
| `2 @ 3` | Lexical error: unsupported character |
| `-.5 + +2 * 3` | Valid; result `5.5` |
| `42` | Valid; result `42`; no operation instructions |

## Viva questions and answers

1. **What is a compiler?**  
   A program that translates source code into another representation, often
   machine code or intermediate code.

2. **What is lexical analysis?**  
   The phase that groups the source characters into tokens.

3. **What is a token?**  
   A meaningful unit such as a number, operator, or parenthesis.

4. **What is a lexeme?**  
   The exact text from the source that forms a token, such as `3.5`.

5. **What does a lexer do with spaces?**  
   MathX ignores whitespace between tokens.

6. **What is syntax analysis?**  
   The phase that checks whether tokens follow the language grammar.

7. **What is a CFG?**  
   A context-free grammar is a set of production rules that describes valid
   language structures.

8. **Why is this grammar context-free?**  
   Each production replaces one non-terminal independently of its surrounding
   symbols.

9. **What is recursive descent parsing?**  
   A top-down parsing technique where methods implement grammar rules and call
   one another.

10. **How does MathX implement operator precedence?**  
    Addition and subtraction are parsed at the `expression` level; multiplication
    and division are parsed deeper at the `term` level.

11. **What is left associativity?**  
    Operators of equal precedence are grouped from left to right. For example,
    `8 / 4 / 2` is parsed as `(8 / 4) / 2`.

12. **What is an AST?**  
    An Abstract Syntax Tree represents the structure of an expression without
    retaining unneeded punctuation.

13. **What is a leaf node in this AST?**  
    A number node, because it has no child expressions.

14. **Why are parentheses not AST nodes here?**  
    They determine grouping while parsing; the resulting tree already captures
    that grouping.

15. **What does Graphviz do in MathX?**  
    It lays out the AST as a readable node-and-edge diagram.

16. **What is intermediate code?**  
    A representation between source input and a lower-level target, useful for
    making operations explicit.

17. **What is three-address code?**  
    A simple intermediate representation where an instruction uses at most
    three addresses: a destination and up to two operands.

18. **Why does MathX use temporary variables?**  
    Temporaries name intermediate values so later instructions can use them.

19. **What is postorder traversal?**  
    Visiting a node's children before the node itself; this naturally emits
    operands before their operation.

20. **How does MathX detect a missing closing parenthesis?**  
    After parsing the expression inside `(`, the parser expects `)` and reports
    an error if it is absent.

21. **How is division by zero detected?**  
    The evaluator checks the evaluated right operand before performing `/`.

22. **Why not use Python `eval()`?**  
    `eval()` executes Python expressions rather than the project's grammar and
    can run unintended code. MathX evaluates only its explicitly supported AST
    nodes.

23. **What happens when parsing fails?**  
    The compiler reports a syntax error and does not create a tree, 3AC, or
    result.

24. **Can a valid expression still fail to evaluate?**  
    Yes. `8 / 0` is syntactically valid but has a division-by-zero evaluation
    error.

25. **What is outside MathX's scope?**  
    Exponentiation, variables, functions, implicit multiplication, and
    optimization are not implemented.
