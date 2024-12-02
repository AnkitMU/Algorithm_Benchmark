import xml.etree.ElementTree as ET
import json
import random

class UMLMetamodel:
    """Defines the UML metamodel with classes, attributes, and relationships."""
    def __init__(self, xmi_file: str):
        self.classes = {}
        self.relationships = []
        self.load_from_xmi(xmi_file)

    def load_from_xmi(self, xmi_file: str):
        """Parse the XMI file to populate classes and relationships."""
        try:
            tree = ET.parse(xmi_file)
            root = tree.getroot()
            ns = {'uml': 'http://www.eclipse.org/uml2/3.0.0/UML'}

            # Debug: Print the root tag for verification
            print(f"Root tag: {root.tag}")

            # Map class IDs to their names
            class_id_to_name = {}

            # Parse Classes and Attributes
            for class_element in root.findall(".//uml:Class", ns):
                class_name = class_element.get("name")
                class_id = class_element.get("{http://www.omg.org/XMI}id")
                if class_name and class_id:
                    print(f"Found class: {class_name} (ID: {class_id})")  # Debugging
                    class_id_to_name[class_id] = class_name
                    self.classes[class_name] = {}
                    for attribute in class_element.findall(".//uml:Property", ns):
                        attr_name = attribute.get("name")
                        attr_type = attribute.get("type") or "String"  # Default to String
                        if attr_name:
                            print(f"  Attribute: {attr_name} ({attr_type})")  # Debugging
                            self.classes[class_name][attr_name] = attr_type

            # Parse Relationships (Associations)
            for assoc in root.findall(".//uml:Association", ns):
                member_end = assoc.get("memberEnd")
                if member_end:
                    source_id, target_id = member_end.split()
                    source_name = class_id_to_name.get(source_id)  # Map source ID to class name
                    target_name = class_id_to_name.get(target_id)  # Map target ID to class name
                    assoc_name = assoc.get("name", f"{source_name}_to_{target_name}")
                    print(f"Found relationship: {assoc_name} ({source_name} -> {target_name})")  # Debugging
                    if source_name and target_name:
                        self.relationships.append({
                            "source": source_name,  # Use mapped class name
                            "target": target_name,  # Use mapped class name
                            "name": assoc_name
                        })

        except ET.ParseError as e:
            print(f"Error parsing XMI file {xmi_file}: {e}")
        except FileNotFoundError:
            print(f"XMI file {xmi_file} not found.")
        except Exception as e:
            print(f"Unexpected error while loading XMI file: {e}")

    def random_attribute(self, cls):
        """Select a random attribute from a class."""
        if cls in self.classes:
            return random.choice(list(self.classes[cls].keys()))
        return None

    def save_extracted_metamodel(self, filename="extracted_metamodel.json"):
        """Save the extracted metamodel to a JSON file."""
        try:
            # Create data to save
            data = {
                "classes": self.classes,
                "relationships": self.relationships,
            }

            # Save to file
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Extracted metamodel saved to {filename}")

        except Exception as e:
            print(f"Error saving extracted metamodel: {e}")
