from graphviz import Digraph


def test_graphviz():
    dot = Digraph(comment="Test Graph")

    # Add nodes
    dot.node("A", "Node A")
    dot.node("B", "Node B")

    # Add an edge
    dot.edge("A", "B", label="Edge from A to B")

    # Render the graph
    output_file = dot.render("test_graph", view=True, format="png")

    print(f"Graph rendered successfully: {output_file}")


if __name__ == "__main__":
    test_graphviz()
