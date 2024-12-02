import random
from smt_solver import validate_binary_constraint

def generate_constraints(uml_meta, ocl_meta, target_class, attr_type, complexity_level, num_constraints):
    """Generate constraints with SMT validation."""
    constraints = []
    for _ in range(num_constraints):
        try:
            # Generate an AST based on the complexity level
            ast = generate_ast("basic", uml_meta, ocl_meta, target_class, attr_type)
            
            # Validate BinaryNode constraints
            if ast["type"] == "BinaryNode":
                if "value" in ast["right"]:
                    is_valid = validate_binary_constraint(
                        ast["class"],
                        ast["left"]["attribute"],
                        ast["op"],
                        ast["right"]["value"]
                    )
                else:
                    raise ValueError("BinaryNode is missing a valid 'right' value.")
                if is_valid:
                    constraints.append(ast)
                else:
                    print("Skipping invalid constraint due to SMT solver failure.")

            # Directly add UnaryNode and other constraints (e.g., NavigationNode, QuantifierNode)
            elif ast["type"] in ["UnaryNode", "NavigationNode", "QuantifierNode"]:
                constraints.append(ast)
            else:
                raise ValueError(f"Unsupported AST type: {ast['type']}")

        except ValueError as e:
            print(f"Skipping invalid constraint: {e}")
    return constraints

def generate_ast(expr_type, uml_meta, ocl_meta, target_class, attr_type):
    """Generate an Abstract Syntax Tree (AST) for an OCL expression."""
    # Filter valid attributes based on the target class and attribute type
    valid_attributes = {attr: t for attr, t in uml_meta.classes[target_class].items() if t == attr_type}
    if not valid_attributes:
        raise ValueError(f"No attributes of type '{attr_type}' found in class '{target_class}'")

    attribute = random.choice(list(valid_attributes.keys()))

    if expr_type == "basic":
        # Handle String constraints
        if attr_type == "String":
            operator = random.choice(["=", "<>", ".size() = 0", ".size() > 0"])
            if operator in ["=", "<>"]:
                return {
                    "type": "BinaryNode",
                    "class": target_class,
                    "left": {"attribute": attribute},
                    "op": operator,
                    "right": {"value": random.choice(['HR', 'IT', 'Sales', 'Admin'])},  # Random string value
                }
            elif operator in [".size() = 0", ".size() > 0"]:
                size_op = "=" if operator == ".size() = 0" else ">"
                return {
                    "type": "UnaryNode",
                    "class": target_class,
                    "left": {"attribute": attribute},
                    "op": f".size() {size_op}",
                    "right": {"value": 0},  # Empty or non-empty check
                }

        # Handle Integer and Float constraints
        elif attr_type in ["Integer", "Float"]:
            return {
                "type": "BinaryNode",
                "class": target_class,
                "left": {"attribute": attribute},
                "op": ocl_meta.random_operator("basic"),
                "right": {"value": random.randint(1, 100)},  # Random numeric value
            }

    # Unsupported expression type
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")
