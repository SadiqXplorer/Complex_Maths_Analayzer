"""Streamlit interface for MathX, a small arithmetic expression compiler."""

import streamlit as st

from compiler import CompilationResult, compile_expression


st.set_page_config(
    page_title="MathX | Expression Compiler",
    page_icon="∑",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        color-scheme: dark;
        --ink: #eceee7;
        --muted: #a5ada2;
        --line: rgba(202, 211, 191, .13);
        --sage: #b8c5a5;
        --copper: #d3a47b;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 7% 7%, rgba(99, 125, 96, .13), transparent 34rem),
            radial-gradient(ellipse at 92% 10%, rgba(151, 110, 75, .10), transparent 28rem),
            linear-gradient(145deg, #121916 0%, #0c1210 52%, #111713 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: rgba(17, 24, 21, .64);
        border-right: 1px solid var(--line);
        backdrop-filter: blur(24px);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
        background: transparent;
    }
    .hero {
        padding: 1.55rem 0 1.45rem;
    }
    .eyebrow {
        color: var(--copper);
        font: 600 .72rem 'JetBrains Mono', monospace;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .7rem;
    }
    .hero h1 {
        color: var(--ink);
        font-size: clamp(2.15rem, 5vw, 3.45rem);
        line-height: 1.08;
        letter-spacing: -.055em;
        margin: 0;
        font-weight: 700;
    }
    .hero h1 span {
        background: linear-gradient(100deg, #c2cba9 5%, #c4b391 88%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .hero p {
        color: var(--muted);
        max-width: 46rem;
        line-height: 1.7;
        font-size: 1rem;
        margin: .9rem 0 0;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(
            138deg,
            rgba(42, 53, 45, .54),
            rgba(20, 29, 25, .48) 56%,
            rgba(30, 34, 28, .5)
        );
        border: 1px solid var(--line) !important;
        border-radius: 16px !important;
        box-shadow:
            inset 0 1px 0 rgba(238, 241, 224, .055),
            0 18px 50px rgba(0, 0, 0, .2);
        backdrop-filter: blur(22px) saturate(115%);
        -webkit-backdrop-filter: blur(22px) saturate(115%);
        transition: border-color .2s ease, background .2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(202, 211, 191, .2) !important;
    }
    [data-testid="stTextInput"] input {
        background: rgba(9, 15, 12, .58);
        border: 1px solid rgba(202, 211, 191, .17);
        border-radius: 10px;
        color: #eff0e8;
        font: 500 1rem 'JetBrains Mono', monospace;
        min-height: 3.25rem;
        transition: border-color .18s ease, box-shadow .18s ease;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: rgba(184, 197, 165, .62);
        box-shadow: 0 0 0 3px rgba(184, 197, 165, .09);
    }
    [data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #b5c29f, #93a486);
        border: 1px solid rgba(228, 231, 210, .19);
        border-radius: 10px;
        color: #172019;
        font-weight: 700;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, .23),
            0 7px 20px rgba(0, 0, 0, .2);
    }
    [data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-1px);
        filter: brightness(1.06);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, .28),
            0 10px 24px rgba(0, 0, 0, .28);
    }
    [data-testid="stBaseButton-secondary"] {
        border-radius: 10px;
        border-color: rgba(202, 211, 191, .2);
        color: #d2d7ca;
        background: rgba(231, 234, 215, .035);
        transition: background .18s ease, border-color .18s ease;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: rgba(202, 211, 191, .34);
        background: rgba(231, 234, 215, .075);
    }
    [data-testid="stTabs"] button {
        color: var(--muted);
        font-size: .88rem;
        transition: color .18s ease;
    }
    [data-testid="stTabs"] button:hover {
        color: var(--ink);
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--sage);
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background: var(--sage);
    }
    code, pre, .stCode { font-family: 'JetBrains Mono', monospace !important; }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 11px;
        overflow: hidden;
    }
    .stage-label {
        color: var(--muted);
        font: 500 .72rem 'JetBrains Mono', monospace;
        letter-spacing: .03em;
    }
    .result-number {
        color: var(--sage);
        font: 600 clamp(2rem, 6vw, 3.5rem) 'JetBrains Mono', monospace;
        letter-spacing: -.06em;
        padding: .35rem 0;
        overflow-wrap: anywhere;
    }
    .small-note { color: var(--muted); font-size: .86rem; }
    [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] p {
        color: var(--muted);
    }
    [data-testid="stCode"] {
        background: rgba(9, 15, 12, .44);
        border: 1px solid rgba(202, 211, 191, .1);
        border-radius: 10px;
    }
    [data-testid="stAlert"] {
        background: rgba(25, 34, 30, .58);
        border: 1px solid var(--line);
        border-radius: 11px;
        backdrop-filter: blur(14px);
    }
    hr { border-color: var(--line) !important; }
    @media (max-width: 720px) {
        .hero { padding: .8rem 0 1rem; }
        [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 13px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def clear_workspace() -> None:
    st.session_state["expression_input"] = ""
    st.session_state["compilation_result"] = None


def show_pipeline(result: CompilationResult | None) -> None:
    if result is None:
        states = ["Ready"] * 6
    else:
        states = [
            "Passed" if result.lexical_success else "Failed",
            "Passed" if result.syntax_valid else (
                "Failed" if result.lexical_success else "Waiting"
            ),
            "Passed" if result.expression_tree is not None else "Waiting",
            "Passed" if result.expression_tree is not None else "Waiting",
            "Passed" if result.evaluation_success else (
                "Failed" if result.expression_tree is not None else "Waiting"
            ),
            "Clear" if not result.errors else "Review",
        ]
    labels = ["LEXER", "PARSER", "TREE", "3AC", "EVALUATOR", "ERRORS"]
    columns = st.columns(6)
    for column, label, status in zip(columns, labels, states):
        with column:
            st.markdown(f"**{label}**", help=f"{label.title()} pipeline phase")
            st.caption(status)


def show_compilation(result: CompilationResult | None) -> None:
    if result is None:
        st.info("Enter an expression and select **Compile expression** to see each phase.")
        return

    tokens_tab, syntax_tab, tree_tab, code_tab, errors_tab, result_tab = st.tabs(
        ["Tokens", "Syntax", "Parse tree", "Three-address code", "Errors", "Result"]
    )

    with tokens_tab:
        if result.tokens:
            st.dataframe(
                [
                    {
                        "Token": token.kind,
                        "Lexeme": token.value,
                        "Position": token.position + 1,
                    }
                    for token in result.tokens
                ],
                use_container_width=True,
                hide_index=True,
            )
        elif result.lexical_success:
            st.caption("No tokens were produced.")
        else:
            st.caption("Lexical analysis stopped before producing tokens.")

    with syntax_tab:
        if result.syntax_valid:
            st.success("Syntax is valid. The expression matches the grammar.")
            st.code(
                "expression -> term ((+ | -) term)*\n"
                "term       -> unary ((* | /) unary)*\n"
                "unary      -> (+ | -) unary | primary\n"
                "primary    -> NUMBER | ( expression )",
                language="text",
            )
        else:
            st.warning("The parser could not validate this expression.")

    with tree_tab:
        if result.graphviz_source:
            st.graphviz_chart(result.graphviz_source, use_container_width=True)
        else:
            st.caption("A parse tree is available after successful syntax analysis.")

    with code_tab:
        if result.expression_tree is None:
            st.caption("Three-address code is available after parsing.")
        elif result.instructions:
            st.code("\n".join(result.instructions), language="text")
        else:
            st.caption("This expression is a single number; no operations need code.")

    with errors_tab:
        if result.errors:
            for error in result.errors:
                st.error(f"**{error.phase}:** {error}")
        else:
            st.success("No lexical, syntax, or evaluation errors detected.")

    with result_tab:
        if result.evaluation_success:
            st.markdown(f'<div class="result-number">{result.value}</div>', unsafe_allow_html=True)
            st.caption("Expression evaluated by recursively walking the validated syntax tree.")
        elif result.expression_tree is not None:
            st.caption("No final value is available until evaluation succeeds.")
        else:
            st.caption("No final value is available until the expression parses.")


with st.sidebar:
    st.markdown(
        """
        <div class="eyebrow">MATHX / WORKSPACE</div>
        <div style="font-size:1.12rem;font-weight:700;color:#eceee7">Compiler lab</div>
        <p style="color:#a5ada2;font-size:.88rem;line-height:1.6">
        A compact arithmetic compiler built for learning the core phases.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("**Supported operators**")
    st.caption("Addition · subtraction · multiplication · division")
    st.markdown("**Grammar**")
    st.code("expression → term → unary → primary", language="text")
    st.markdown("**Example**")
    st.code("(10 + 5) * 2 - 4", language="text")
    st.caption("Parentheses and unary + / - are supported.")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">B.TECH · COMPILER DESIGN PROJECT</div>
      <h1>MathX <span>Expression Compiler</span></h1>
      <p>Trace an arithmetic expression through tokenization, recursive-descent parsing,
      syntax-tree generation, intermediate code, and safe evaluation.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown("#### Expression editor")
    left, right = st.columns([5, 1])
    with left:
        st.text_input(
            "Mathematical expression",
            placeholder="Try: (10 + 5) * 2 - 4",
            key="expression_input",
            label_visibility="collapsed",
        )
    with right:
        st.markdown("<div style='height:1.82rem'></div>", unsafe_allow_html=True)
        st.button(
            "Clear",
            use_container_width=True,
            on_click=clear_workspace,
        )
    compile_column, hint_column = st.columns([1, 4])
    with compile_column:
        compile_clicked = st.button(
            "Compile expression",
            type="primary",
            use_container_width=True,
        )
    with hint_column:
        st.markdown(
            '<div class="small-note" style="padding:.65rem 0">'
            "Numbers, +, -, *, /, and parentheses · no Python eval/exec"
            "</div>",
            unsafe_allow_html=True,
        )

if compile_clicked:
    st.session_state["compilation_result"] = compile_expression(
        st.session_state.get("expression_input", "")
    )

compilation_result = st.session_state.get("compilation_result")
st.markdown("#### Compiler pipeline")
show_pipeline(compilation_result)
st.divider()
st.markdown("#### Compilation output")
show_compilation(compilation_result)
