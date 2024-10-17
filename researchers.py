from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF, RDF

# Create a Graph
g = Graph()

# Define the namespace for our users (we'll use the example.com domain for illustration)
EX = Namespace("http://example.com/users/")

# Bind the FOAF namespace to a prefix for easier reference
g.bind("foaf", FOAF)
g.bind("membr", EX)

# Function to add a user to the graph
def add_user(last_name, first_name, project_name):
    # Remove all blank spaces from the last name
    last_name_cleaned = last_name.replace(" ", "")
    last_name_cleaned = last_name_cleaned.replace("-", "")
    last_name_cleaned = last_name_cleaned.replace("ß", "ss")
    last_name_cleaned = last_name_cleaned.replace("á", "a")

    # Create a URI for the user based on their last name
    user_uri = EX[last_name_cleaned]
    # Create a URI for the projects based on the last name of the researcher
    project_uri = EX[f'Project_{last_name_cleaned}']

    # Add RDF triples to the graph
    # related to users
    g.add((user_uri, RDF.type, FOAF.Person))
    g.add((user_uri, FOAF.familyName, Literal(last_name)))
    g.add((user_uri, FOAF.givenName, Literal(first_name)))
    g.add((user_uri, FOAF.currentProject, project_uri))
    # related to projects
    g.add((project_uri, RDF.type, EX.Project))
    g.add((project_uri, EX.projectName, Literal(project_name, lang = "en")))

# Add users to the graph
add_user("Blake", "Ashley", "Project Blake")
add_user("De la Garza", "Vania", "Project De la Garza")
add_user("Fernández Santos", "Sara", "Artificial language learning as a window to the early entrenchment of constructions")
add_user("Fokashchuk", "Iryna", "Functions and cognitive semantics of prepositions in complex constructions")
add_user("Führer", "Bastian", "German verbs with particles or prefixes in language change: Form, meaning, and syntax")
add_user("Gedik", "Tan Arda", "Project Gedik")
add_user("Grose-Hodge", "Magdalena Grose-Hodge", "Project Grose-Hodge")
add_user("Iabdounane", "Yassine", "Multimodal constructional space")
add_user("Kassler", "Annika", "Project Kassler")
add_user("Kenanidis", "Panagiotis", "Project Kenanidis")
add_user("Keßler", "Florian", "Project Keßler")
add_user("Kissane", "Hassane", "Form and meaning as factors in the identification and learning of constructional slots – English phrasal verbs and verb-preposition combinations")
add_user("Kligge", "Hendrik", "Representation and acquisition of agreement relations in a usage-based framework")
add_user("Lee", "Dongeun", "Project Lee")
add_user("Patel", "Malin", "Corpus evidence for delineating constructions")
add_user("Prela", "Leonarda", "Project Prela")
add_user("Ramezani", "Pegah", "Representation and processing of constructions in the brain")
add_user("Rastegar", "Aria", "Representation and acquisition of idiomatic constructions in L1 and L2 learners")
add_user("Legouté", "Anne Sherley", "Multifunctionality in Haitian Creole: New insights from a Construction Grammar perspective")
add_user("Stampfer", "Veronika", "Semantically related argument structures in the history of English")
add_user("Trombetta", "Chiara", "Constructions beyond the sentence: text-structuring in (esp.) sixteenth-century historiographical texts")
add_user("Wright", "Richenda", "Project Wright")
add_user("Winckel", "Elodie", "Building a Research Constructicon")

# Serialize the graph in Turtle format and write to a file
output_file = "users.ttl"
with open(output_file, "w") as f:
    f.write(g.serialize(format="turtle"))

print(f"The RDF graph has been exported to {output_file}")