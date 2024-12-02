from ast_generator import generate_ast

def generate_constraints(uml_meta, ocl_meta, target_class, attr_type, complexity_level, num_constraints):
    """Generate constraints based on user-defined complexity level and attributes."""
    from ast_generator import generate_ast  # Moved inside the function to avoid circular import

    constraints = []
    for _ in range(num_constraints):
        try:
            if complexity_level == 1:
                constraints.append(generate_ast("basic", uml_meta, ocl_meta, target_class, attr_type))
            elif complexity_level == 2:
                constraints.append(generate_ast("navigation", uml_meta, ocl_meta, target_class, attr_type))
            elif complexity_level == 3:
                constraints.append(generate_ast("collection", uml_meta, ocl_meta, target_class, attr_type))
            elif complexity_level == 4:
                constraints.append(generate_ast("quantifiers", uml_meta, ocl_meta, target_class, attr_type))
            else:
                raise ValueError("Unsupported complexity level")
        except ValueError as e:
            print(f"Skipping invalid constraint: {e}")
    return constraints
