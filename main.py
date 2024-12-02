from uml_metamodel import UMLMetamodel
from metamodel import OCLMetamodel
from constraint_levels import generate_constraints
from ocl_formatter import format_constraint, save_constraints
from smt_solver import validate_binary_constraint

def main():
    # Load UML Metamodel
    xmi_file = "model.xmi"
    uml_meta = UMLMetamodel(xmi_file)
    ocl_meta = OCLMetamodel()

    # Display available classes and attributes
    print("\nAvailable Classes and Attributes:")
    for cls, attrs in uml_meta.classes.items():
        print(f"Class: {cls}")
        for attr, attr_type in attrs.items():
            print(f"  - {attr}: {attr_type}")

    # Choose the class
    print("\nSelect the class to generate constraints:")
    classes = list(uml_meta.classes.keys())
    for i, cls in enumerate(classes, start=1):
        print(f"{i}: {cls}")
    class_choice = int(input("\nEnter the number corresponding to your choice: "))
    target_class = classes[class_choice - 1]

    # Choose the attribute type
    print("\nSelect the type of attributes for constraints:")
    attr_types = {t for attr, t in uml_meta.classes[target_class].items()}
    attr_types = list(attr_types)
    for i, attr_type in enumerate(attr_types, start=1):
        print(f"{i}: {attr_type}")
    attr_choice = int(input("\nEnter the number corresponding to your choice: "))
    attr_type = attr_types[attr_choice - 1]

    # Choose the complexity level
    print("\nSelect the complexity level:")
    complexity_levels = ["Simple", "Navigation", "Collection", "Quantifiers"]
    for i, level in enumerate(complexity_levels, start=1):
        print(f"{i}: {level}")
    complexity_choice = int(input("\nEnter the number corresponding to your choice: "))
    complexity_level = complexity_choice

    # Choose the number of constraints
    num_constraints = int(input("\nEnter the number of constraints to generate: "))

    # Generate constraints
    print("\nGenerating OCL constraints...")
    raw_constraints = generate_constraints(uml_meta, ocl_meta, target_class, attr_type, complexity_level, num_constraints)

    # Validate constraints with SMT solver
    valid_constraints = []
    for ast in raw_constraints:
        if ast["type"] == "BinaryNode":
            is_valid = validate_binary_constraint(
                ast["class"],
                ast["left"]["attribute"],
                ast["op"],
                ast["right"]["value"]
            )
            if is_valid:
                valid_constraints.append(ast)
            else:
                print(f"Skipping invalid constraint: {ast}")
        else:
            # Handle other constraint types (e.g., navigation, quantifiers) here if needed
            valid_constraints.append(ast)

    # Format and save constraints
    formatted_constraints = [
        format_constraint(ast, f"Constraint{i+1}") for i, ast in enumerate(valid_constraints)
    ]
    save_constraints(formatted_constraints, "generated_constraints.ocl")

    print("\nGenerated Constraints:")
    for constraint in formatted_constraints:
        print(constraint)

if __name__ == "__main__":
    main()
