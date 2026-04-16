from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF, RDF

# Create a Graph
g = Graph()

# Define the namespace for our users (we'll use the example.com domain for illustration)
membr = Namespace("http://example.org/users#")
rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")

# Bind the FOAF namespace to a prefix for easier reference
g.bind("foaf", FOAF)
g.bind("membr", membr)
g.bind("rsrch", rsrch)

# Function to add a user to the graph
def add_user(last_name, first_name, project_name):
    # Remove all blank spaces from the last name
    last_name_cleaned = last_name.replace(" ", "")
    last_name_cleaned = last_name_cleaned.replace("-", "")
    last_name_cleaned = last_name_cleaned.replace("ß", "ss")
    last_name_cleaned = last_name_cleaned.replace("á", "a")
    last_name_cleaned = last_name_cleaned.replace("é", "e")
    last_name_cleaned = last_name_cleaned.replace("ü", "ue")

    # Create a URI for the user based on their last name
    user_uri = membr[last_name_cleaned]
    # Create a URI for the projects based on the last name of the researcher
    project_uri = membr[f'Project_{last_name_cleaned}']

    # Add RDF triples to the graph
    # related to users
    g.add((user_uri, RDF.type, FOAF.Person))
    g.add((user_uri, FOAF.familyName, Literal(last_name)))
    g.add((user_uri, FOAF.givenName, Literal(first_name)))
    g.add((user_uri, FOAF.currentProject, project_uri))
    # related to projects
    g.add((project_uri, RDF.type, rsrch.Project))
    g.add((project_uri, rsrch.projectName, Literal(project_name, lang = "en")))

# Add users to the graph
add_user("Alhabyan", "Raghad", "Project Alhabyan")
add_user("Badawi", "Soran", "Project Badawi")
add_user("Bayer", "Nadine", "Project Bayer")
add_user("Benito Fernandez", "Elba", "Project Benito Fernandez")
add_user("Blake", "Ashley", "Project Blake")
add_user("Boos", "Julia", "Project Boos")
add_user("De la Garza", "Vania", "Project De la Garza")
add_user("Fernández Santos", "Sara", "Artificial language learning as a window to the early entrenchment of constructions")
add_user("Fokashchuk", "Iryna", "Functions and cognitive semantics of prepositions in complex constructions")
add_user("Führer", "Bastian", "German verbs with particles or prefixes in language change: Form, meaning, and syntax")
add_user("Gedik", "Tan Arda", "Project Gedik")
add_user("Gromadsky", "Dmitry", "Project Gromadsky")
add_user("Grose-Hodge", "Magdalena", "Project Grose-Hodge")
add_user("Hutta", "Sophie", "Project Hutta")
add_user("Iabdounane", "Yassine", "Multimodal constructional space")
add_user("Immertreu", "Mathis", "Project Immertreu")
add_user("Kashigin", "Kyra", "Project Kashigin")
add_user("Kassler", "Annika", "Project Kassler")
add_user("Kenanidis", "Panagiotis", "Project Kenanidis")
add_user("Keßler", "Florian", "Chinese Mathematics")
add_user("Khanoub", "Rania", "Project Khanoub")
add_user("Kissane", "Hassane", "Form and meaning as factors in the identification and learning of constructional slots – English phrasal verbs and verb-preposition combinations")
add_user("Kligge", "Hendrik", "Representation and acquisition of agreement relations in a usage-based framework")
add_user("Lee", "Dongeun", "Project Lee")
add_user("Makhanina", "Asia", "Project Makhanina")
add_user("Patel", "Malin", "Corpus evidence for delineating constructions")
add_user("Petrenko", "Elizaveta", "Project Petrenko")
add_user("Prela", "Leonarda", "Project Prela")
add_user("Ramezani", "Pegah", "Representation and processing of constructions in the brain")
add_user("Rastegar", "Aria", "Representation and acquisition of idiomatic constructions in L1 and L2 learners")
add_user("Rohwedder", "Paul", "Project Rohwedder")
add_user("Legouté", "Anne Sherley", "Multifunctionality in Haitian Creole: New insights from a Construction Grammar perspective")
add_user("Schmechel", "Dennis", "Project Schmechel")
add_user("Senger", "Lena", "Project Senger")
add_user("Stampfer", "Veronika", "Semantically related argument structures in the history of English")
add_user("Trombetta", "Chiara", "Constructions beyond the sentence: text-structuring in (esp.) sixteenth-century historiographical texts")
add_user("Tzimas", "Theocharis", "Project Tzimas")
add_user("Wright", "Richenda", "Project Wright")
add_user("Weigelt", "Lina", "Project Weigelt")
add_user("Winckel", "Elodie", "Building a Research Constructicon")

# Serialize the graph in Turtle format and write to a file
output_file = "../Abox/membr.ttl"
with open(output_file, "w") as f:
    f.write(g.serialize(format="turtle"))

print(f"The RDF graph has been exported to {output_file}")