import xml.etree.ElementTree as ET

file_path = 'model.xmi'
output_file_path = 'model.use'

ns = {'uml': 'http://www.eclipse.org/uml2/3.0.0/UML'}

def extract_classes(root, use_file, class_id_to_name):
    for class_element in root.findall('.//uml:Class', ns):
        class_name = class_element.get('name')
        class_id = class_element.get('{http://www.omg.org/XMI}id')
        class_id_to_name[class_id] = class_name  # Map ID to class name

        use_file.write(f"class {class_name}\nattributes\n")
        for attribute in class_element.findall('.//uml:Property', ns):
            attr_name = attribute.get('name')
            attr_type = attribute.get('type') or "Unknown"
            if attr_type == "Float":
                attr_type = "Real"  # USE uses Real instead of Float
            use_file.write(f"  {attr_name}:{attr_type}\n")
        use_file.write("operations\n")
        for operation in class_element.findall('.//uml:Operation', ns):
            operation_name = operation.get('name')
            use_file.write(f"  {operation_name}()\n")
        use_file.write("end\n\n")

def extract_associations(root, use_file, class_id_to_name):
    for association in root.findall('.//uml:Association', ns):
        assoc_id = association.get('{http://www.omg.org/XMI}id')
        owned_ends = association.findall('uml:ownedEnd', ns)

        if owned_ends:
            use_file.write(f"association Association_{assoc_id} between\n")
            for end in owned_ends:
                end_type = end.get('type')
                end_type_name = class_id_to_name.get(end_type, "UnknownClass")
                multiplicity = "[0..*]"  # Default multiplicity if not defined
                role_name = f"role {end_type_name.lower()}Role"
                use_file.write(f"  {end_type_name} {multiplicity} {role_name}\n")
            use_file.write("end\n\n")

def main():
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        class_id_to_name = {}

        with open(output_file_path, 'w') as use_file:
            use_file.write("model ExtractedModel\n\n")
            extract_classes(root, use_file, class_id_to_name)
            use_file.write("-- associations\n\n")
            extract_associations(root, use_file, class_id_to_name)
            #use_file.write("\n")
        
        print(f"Model successfully written to {output_file_path}")

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
