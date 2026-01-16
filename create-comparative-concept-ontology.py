from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, XSD, SKOS
from rdflib.namespace import DC, DCTERMS
import yaml

# Define namespaces
compcon = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#")
cx = Namespace("http://example.org/cx/")

# Load YAML content
with open('/home/meuhlodi/Travail/RCxn/ontologies/cc-database.yaml', 'r') as file:
    database = yaml.safe_load(file)

g = Graph()
g.bind("compcon", compcon)
g.bind("cx", cx)

# Define class "Comparative concept"
g.add((compcon.compcon, RDF.type, RDFS.Class))
g.add((compcon.compcon, RDFS.label, Literal("Comparative concept")))

# Define subclasses of "Comparative concept"
g.add((compcon.sem, RDF.type, RDFS.Class))
g.add((compcon.sem, RDFS.label, Literal("meaning")))
g.add((compcon.sem, RDFS.subClassOf, compcon.compcon))
g.add((compcon.inf, RDF.type, RDFS.Class))
g.add((compcon.inf, RDFS.label, Literal("information packaging")))
g.add((compcon.inf, RDFS.subClassOf, compcon.compcon))
g.add((compcon.str, RDF.type, RDFS.Class))
g.add((compcon.str, RDFS.label, Literal("strategy")))
g.add((compcon.str, RDFS.subClassOf, compcon.compcon))
g.add((compcon.cxn, RDF.type, RDFS.Class))
g.add((compcon.cxn, RDFS.label, Literal("construction")))
g.add((compcon.cxn, RDFS.subClassOf, compcon.compcon))

# Define some properties introduced in the yaml database
g.add((compcon.subtypeOf, RDF.type, RDF.Property))
g.add((compcon.subtypeOf, RDFS.label, Literal("Subtype of")))
g.add((compcon.functionOf, RDF.type, RDF.Property))
g.add((compcon.functionOf, RDFS.label, Literal("Function of")))
g.add((compcon.roleOf, RDF.type, RDF.Property))
g.add((compcon.roleOf, RDFS.label, Literal("Role of")))
g.add((compcon.ExpressionOf, RDF.type, RDF.Property))
g.add((compcon.ExpressionOf, RDFS.label, Literal("Expresses")))
g.add((compcon.language, RDF.type, RDF.Property))
g.add((compcon.language, RDFS.label, Literal("Language")))

# Define property hasCompCon which will be used to annotate construction entries
g.add((compcon.hasCompCon, RDF.type, RDF.Property))
g.add((compcon.hasCompCon, RDFS.label, Literal("Comparative Concept")))

def add_entry_to_graph(entry):
    entry_id = entry['Id']
    entry_type = entry['Type']

    # Create URI for the entry
    entry_uri = compcon[str.replace(entry_id,":","_")]

    # Add type of comparative concept (sem, inf, cxn, str)
    g.add((entry_uri, RDF.type, compcon[entry_type]))

    # Add name
    g.add((entry_uri, RDFS.label, Literal(entry['Name'])))

    # Add alias
    if 'Alias' in entry:
        for alias in entry['Alias']:
            g.add((entry_uri, SKOS.altLabel, Literal(alias)))

    # Add SubtypeOf
    if 'SubtypeOf' in entry:
        for subtype in entry['SubtypeOf']:
            g.add((entry_uri, compcon.subtypeOf, compcon[str.replace(subtype,":","_")]))

    # Add FunctionOf
    if 'FunctionOf' in entry:
        for function in entry['FunctionOf']:
            g.add((entry_uri, compcon.functionOf, compcon[str.replace(function,":","_")]))

    # Add RoleOf
    if 'RoleOf' in entry:
        for role in entry['RoleOf']:
            g.add((entry_uri, compcon.roleOf, compcon[str.replace(role,":","_")]))

    # Add ExpressionOf
    if 'ExpressionOf' in entry:
        for expression in entry['ExpressionOf']:
            g.add((entry_uri, compcon.expressionOf, compcon[str.replace(expression,":","_")]))

    # Add Definition
    g.add((entry_uri, DC.description, Literal(entry['Definition'])))

    # Add Sections
    if 'Sections' in entry:
        for section in entry['Sections']:
            g.add((entry_uri, DCTERMS.isPartOf, Literal(section)))

    # Add Examples
    if 'Examples' in entry:
        for i, example in enumerate(entry['Examples']):
            if isinstance(example, str):
                example_uri = URIRef(f"{compcon}{entry_id.split(':')[1]}-example-{i}")
                g.add((example_uri, RDF.type, cx.Example))
                g.add((example_uri, RDFS.label, Literal(example)))
                g.add((entry_uri, cx.hasExample, example_uri))
            elif isinstance(example, dict):
                example_uri = URIRef(f"{compcon}{entry_id.split(':')[1]}-example-{i}")
                g.add((example_uri, RDF.type, cx.Example))
                g.add((example_uri, compcon.language, Literal(example['Language'])))
                g.add((example_uri, RDFS.label, Literal(example['Example'])))
                #if example['Gloss']:
                #    gloss_literal = str(example['Gloss'])
                #    print(gloss_literal)
                #    g.add((example_uri, cx.gloss, Literal(gloss_literal)))
                #g.add((example_uri, cx.translation, Literal(example['Translation'])))
                g.add((entry_uri, cx.hasExample, example_uri))

# Add each entry to the graph
for entry in database:
    add_entry_to_graph(entry)

# Serialize the graph to Turtle format
ttl_content = g.serialize(format='turtle')

# Save the Turtle content to a file
with open('/home/meuhlodi/Travail/RCxn/ontologies/compcon.ttl', 'w') as f:
    f.write(ttl_content)
