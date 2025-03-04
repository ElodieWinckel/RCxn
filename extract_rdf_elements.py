import re


def extract_rdf_elements_from_python(file_path, output_file):
    with open(file_path, 'r') as file:
        code = file.read()

    # Patterns to capture RDF elements (namespaces, classes, and properties)
    namespaces_pattern = re.compile(r"Namespace\(['\"](.+?)['\"]\)")
    rdf_type_pattern = re.compile(r"RDF\.type, (.+?)[\)\,]")
    predicates_pattern = re.compile(r"g.add\(.+?, (.+?), .+?\)")

    # Using sets to avoid duplicates
    namespaces = set(namespaces_pattern.findall(code))
    classes = set(rdf_type_pattern.findall(code))
    predicates = set(predicates_pattern.findall(code))

    # Write the results to a text file
    with open(output_file, 'w') as out_file:
        out_file.write("Namespaces used:\n")
        for ns in sorted(namespaces):  # Sort for readability
            out_file.write(ns + '\n')

        out_file.write("\nClasses declared (rdf:type):\n")
        for cls in sorted(classes):  # Sort for readability
            out_file.write(cls + '\n')

        out_file.write("\nProperties used (predicates):\n")
        for prop in sorted(predicates):  # Sort for readability
            out_file.write(prop + '\n')


# Example usage
python_file = "app_form/routes.py"  # Replace with the path to your Python file
output_file = "rdf_elements_output.txt"  # File where results will be saved

extract_rdf_elements_from_python(python_file, output_file)

print(f"RDF elements have been written to {output_file}")
