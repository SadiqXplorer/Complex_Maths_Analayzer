"""Abstract syntax tree node definitions and Graphviz rendering."""

from dataclasses import dataclass

from graphviz import Digraph


@dataclass(frozen=True)
class Number:
    value: int | float
    lexeme: str
    position: int


@dataclass(frozen=True)
class UnaryOperation:
    operator: str
    operand: "Expression"
    position: int


@dataclass(frozen=True)
class BinaryOperation:
    operator: str
    left: "Expression"
    right: "Expression"
    position: int


Expression = Number | UnaryOperation | BinaryOperation


def to_graphviz(expression: Expression) -> Digraph:
    """Build a Graphviz directed graph for an expression tree."""
    graph = Digraph("expression_tree")
    graph.attr(
        "graph",
        bgcolor="transparent",
        rankdir="TB",
        nodesep="0.55",
        ranksep="0.7",
        pad="0.2",
    )
    graph.attr(
        "node",
        fontname="DM Sans",
        fontsize="13",
        style="filled",
        color="#899681",
        fontcolor="#eceee7",
        fillcolor="#29352d",
        penwidth="1.4",
    )
    graph.attr("edge", color="#a1ad91", penwidth="1.4", arrowsize="0.7")
    next_id = 0

    def add_node(node: Expression) -> str:
        nonlocal next_id
        node_id = f"n{next_id}"
        next_id += 1

        if isinstance(node, Number):
            graph.node(
                node_id,
                label=node.lexeme,
                shape="ellipse",
                fillcolor="#253129",
            )
        elif isinstance(node, UnaryOperation):
            graph.node(
                node_id,
                label=f"unary {node.operator}",
                shape="circle",
                fillcolor="#574536",
            )
            child_id = add_node(node.operand)
            graph.edge(node_id, child_id)
        else:
            graph.node(
                node_id,
                label=node.operator,
                shape="circle",
                fillcolor="#354333",
            )
            left_id = add_node(node.left)
            right_id = add_node(node.right)
            graph.edge(node_id, left_id)
            graph.edge(node_id, right_id)
        return node_id

    add_node(expression)
    return graph
