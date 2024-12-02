from typing import Dict

def format_constraint(ast, invariant_name):
    """Format a constraint with context and invariant."""
    class_name = ast.get("class", "Unknown")
    constraint = format_ocl(ast)
    return f"context {class_name}\n    inv {invariant_name}: {constraint}"

def save_constraints(constraints, filename):
    """Save constraints to a file."""
    with open(filename, "w") as file:
        for constraint in constraints:
            file.write(constraint + "\n\n")
    print(f"Constraints saved to {filename}")

def format_ocl(ast):
    """Format an Abstract Syntax Tree (AST) into OCL syntax."""
    if ast["type"] == "BinaryNode":
        # Format binary operations (e.g., self.attribute > value)
        left = ast["left"]["attribute"]
        op = ast["op"]
        right = ast["right"]["value"]
        # Add quotes for string values
        if isinstance(right, str) and not right.startswith("'"):
            right = f"'{right}'"
        return f"self.{left} {op} {right}"

    elif ast["type"] == "UnaryNode":
        # Format unary operations (e.g., self.attribute.size() > 0)
        left = ast["left"]["attribute"]
        op = ast["op"]
        right = ast["right"]["value"]
        return f"self.{left}{op} {right}"

    elif ast["type"] == "NavigationNode":
        # Format navigation operations (e.g., self.relationship.attribute op value)
        relationship = ast["relationship"]
        attribute = ast["attribute"]
        op = ast["op"]
        return f"self.{relationship}.{attribute} {op}"

    elif ast["type"] == "QuantifierNode":
        # Format quantifier operations (e.g., self.relationship->forall(condition))
        quantifier = ast["quantifier"]
        relationship = ast["relationship"]
        condition = format_ocl(ast["condition"])  # Recursively format the condition
        return f"self.{relationship}->{quantifier}({condition})"

    else:
        raise ValueError(f"Unknown AST type: {ast['type']}")
