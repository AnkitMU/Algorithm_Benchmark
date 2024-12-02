from z3 import *

def validate_binary_constraint(class_name, attribute, operator, value):
    """Validate a simple binary constraint using an SMT solver."""
    solver = Solver()

    # Define Z3 variables for the attribute based on the value type
    if isinstance(value, int):
        attr = Int(attribute)
        solver.add(attr >= 0)  # Ensure non-negative values for numeric attributes
    elif isinstance(value, str):
        attr = String(attribute)
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

    # Numeric operators
    if operator in [">", ">=", "<", "<=", "="]:
        if isinstance(value, int):
            if operator == ">":
                solver.add(attr > value)
            elif operator == ">=":
                solver.add(attr >= value)
            elif operator == "<":
                solver.add(attr < value)
            elif operator == "<=":
                solver.add(attr <= value)
            elif operator == "=":
                solver.add(attr == value)
        else:
            raise ValueError(f"Invalid value for numeric operator '{operator}'; expected a numeric value.")

    # String operators
    elif operator in ["=", "<>"]:
        if isinstance(value, str):
            if operator == "=":
                solver.add(attr == value)
            elif operator == "<>":
                solver.add(attr != value)
        else:
            raise ValueError(f"Invalid value for string operator '{operator}'; expected a string value.")

    # Logical operators
    elif operator in ["and", "or"]:
        if isinstance(value, list) and len(value) == 2:
            condition1 = attr == value[0]
            condition2 = attr == value[1]
            if operator == "and":
                solver.add(And(condition1, condition2))
            elif operator == "or":
                solver.add(Or(condition1, condition2))
        else:
            raise ValueError(f"Invalid value for logical operator '{operator}'; must provide a list of two conditions.")
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    # Check satisfiability
    if solver.check() == sat:
        print(f"[VALID] {class_name}.{attribute} {operator} {value}")
        return True
    else:
        print(f"[INVALID] {class_name}.{attribute} {operator} {value}")
        return False

# Debugging Function for Logging
def debug_constraint(class_name, attribute, operator, value):
    """Log the constraint details for debugging purposes."""
    print(f"Debugging Constraint: {class_name}.{attribute} {operator} {value}")
