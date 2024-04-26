from graphviz import Digraph
import re
import os

# Define colors for different gate types
gate_colors = {
    "inp": "skyblue",
    "out": "yellow",
    "and2": "purple",
    "not": "salmon",
    "or2": "lightgreen",
}

gate_shapes = {
    "inp": "circle",
    "out": "circle",
    "and2": "square",
    "not": "invtriangle",
    "or2": "diamond",
}

def display(circ, dir, gen):
    dir_copy = dir
    dir = os.path.join(dir, gen)
    circ = os.path.join(dir, circ+".py")

    with open(circ, "r") as file:
        content = file.read()

    dot = Digraph()

    gate_pattern = re.compile(r'GATE\s*\(\s*"([^"]+)"\s*,\s*type\s*=\s*"([^"]+)"\s*\)')
    wire_pattern = re.compile(r'WIRE\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')

    # Find and process gate definitions
    gate_matches = gate_pattern.findall(content)
    for name, gate_type in gate_matches:
        node_name = f"{name}_{gate_type}"
        dot.node(name, label=name, shape=gate_shapes.get(gate_type), color=gate_colors.get(gate_type, "white"))

    # Find and process wire connections
    wire_matches = wire_pattern.findall(content)
    for src, dest in wire_matches:
        #dot.edge(src, dest)
        # Split the source and destination strings into gate names and ports
        src_split = src.split("/")
        src_gate = src_split[0]

        dest_split = dest.split("/")
        dest_gate = dest_split[0]

        dot.edge(src_gate, dest_gate)

    # Save the graph to a file
    circ = os.path.join(dir_copy, "final")
    dot.render(circ, format="png", cleanup=True)
    