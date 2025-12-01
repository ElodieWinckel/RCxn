from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, RDF
import glob

# File paths
output_cx = "Abox/cx.ttl"
output_membr = "Abox/users.ttl"

# Create general graph, and subgraphs holders for cx and membr
g = Graph()
graph_cx = Graph()
graph_membr = Graph()

# Load everything from the submissions (assuming that everything in the submission folder has now a green light)
for ttl_file in glob.glob("instance/Submissions/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Namespaces
cx = Namespace("http://example.org/cx/")
g.bind("cx", cx)
graph_cx.bind("cx", cx)
graph_membr.bind("cx", cx)

membr = Namespace("http://example.org/users#")
g.bind("membr", membr)
graph_cx.bind("membr", membr)
graph_membr.bind("membr", membr)

rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
g.bind("rcxn", rcxn)
graph_cx.bind("rcxn", rcxn)
graph_membr.bind("rcxn", rcxn)

rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
g.bind("rsrch", rsrch)
graph_cx.bind("rsrch", rsrch)
graph_membr.bind("rsrch", rsrch)

links = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links-1.0#")
g.bind("links", links)
graph_cx.bind("links", links)
graph_membr.bind("links", links)

olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
graph_cx.bind("olia", olia)
graph_membr.bind("olia", olia)

oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
g.bind("oliatop", oliatop)
graph_cx.bind("oliatop", oliatop)
graph_membr.bind("oliatop", oliatop)

rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
g.bind("rdfs", rdfs)
graph_cx.bind("rdfs", rdfs)
graph_membr.bind("rdfs", rdfs)

lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
g.bind("lg", lg)
graph_cx.bind("lg", lg)
graph_membr.bind("lg", lg)

rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
g.bind("rdf_ns", rdf_ns)
graph_cx.bind("rdf_ns", rdf_ns)
graph_membr.bind("rdf_ns", rdf_ns)

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
add_user("Alhabyan", "Raghad", "Valency, preposition governing, and phrasal verbs in Arabic and Semitic")
add_user("Badawi", "Soran", "Corpus-based measures of constructionhood")
add_user("Bayer", "Nadine", "Project Bayer")
add_user("Benito Fernandez", "Elba", "Spanish quotative constructions in oral narratives — an Interactional Construction Grammar approach")
add_user("Blake", "Ashley", "Project Blake")
add_user("Boos", "Julia", "Entrenchment meets literacy: How the development of reading ability affects child and adult language processing")
add_user("De la Garza", "Vania", "Project De la Garza")
add_user("Fernández Santos", "Sara", "Artificial language learning as a window to the early entrenchment of constructions")
add_user("Fokashchuk", "Iryna", "Functions and cognitive semantics of prepositions in complex constructions")
add_user("Führer", "Bastian", "German verbs with particles or prefixes in language change: Form, meaning, and syntax")
add_user("Gedik", "Tan Arda", "Project Gedik")
add_user("Gromadsky", "Dmitry", "Constructions in communication")
add_user("Grose-Hodge", "Magdalena", "Project Grose-Hodge")
add_user("Hutta", "Sophie", "Project Hutta")
add_user("Iabdounane", "Yassine", "Multimodal constructional space")
add_user("Immertreu", "Mathis", "Multimodal cognitive maps for cross-domain constructional networks")
add_user("Kashigin", "Kyra", "Contrastive Construction Grammar: The interaction of argument-structure constructions and sentence-type constructions in english, Dutch and German")
add_user("Kassler", "Annika", "Project Kassler")
add_user("Kenanidis", "Panagiotis", "Project Kenanidis")
add_user("Keßler", "Florian", "Chinese Mathematics")
add_user("Khanoub", "Rania", "Project Khanoub")
add_user("Kissane", "Hassane", "Form and meaning as factors in the identification and learning of constructional slots – English phrasal verbs and verb-preposition combinations")
add_user("Kligge", "Hendrik", "Representation and acquisition of agreement relations in a usage-based framework")
add_user("Lee", "Dongeun", "Project Lee")
add_user("Makhanina", "Asia", "Representation and acquisition of idiomatic constructions in L1 and L2 learners")
add_user("Patel", "Malin", "Corpus evidence for delineating constructions")
add_user("Petrenko", "Elizaveta", "Comparing constructions cross-linguistically — Connecting constructicons")
add_user("Prela", "Leonarda", "Project Prela")
add_user("Ramezani", "Pegah", "Representation and processing of constructions in the brain")
add_user("Rastegar", "Aria", "Representation and acquisition of idiomatic constructions in L1 and L2 learners")
add_user("Rohwedder", "Paul", "Project Rohwedder")
add_user("Legouté", "Anne Sherley", "Multifunctionality in Haitian Creole: New insights from a Construction Grammar perspective")
add_user("Schmechel", "Dennis", "Project Schmechel")
add_user("Senger", "Lena", "Project Senger")
add_user("Stampfer", "Veronika", "Semantically related argument structures in the history of English")
add_user("Trombetta", "Chiara", "Constructions beyond the sentence: text-structuring in (esp.) sixteenth-century historiographical texts")
add_user("Tzimas", "Theocharis", "Subject-inversion throughout Early Modern English: changing relations in individual and communal constructions")
add_user("Wright", "Richenda", "Project Wright")
add_user("Weigelt", "Lina", "Project Weigelt")
add_user("Winckel", "Elodie", "Building a Research Constructicon")

# If some construction uses another construction as construction element, then link back the second construction to the first one
for construction in g.subjects(rdf_ns.type, rcxn.Construction):
    # Get the sequence of slots
    for sequence in g.objects(construction, rcxn.hasSlots):
        # RDF collections are often numbered rdf:_1, rdf:_2, etc.
        for slot_pred, slot in g.predicate_objects(sequence):
            if str(slot_pred).startswith(str(rdf_ns["_"])):
                # Get the slot form
                for form in g.objects(slot, rcxn.hasSlotForm):
                    # Get the syntactic form (part)
                    for part in g.objects(form, rcxn.hasSyntacticForm):
                        # Add new triple: ?part rcxn:elementOf ?construction
                        g.add((part, rcxn.elementOf, construction))

for mainCX in g.subjects(rdf_ns.type, rcxn.Construction):
    # identify inheritsFrom links
    for linkedCX in g.objects(mainCX, links.inheritsFrom):
        g.add((linkedCX, links.inheritedBy, mainCX))

for mainCX in g.subjects(rdf_ns.type, rcxn.Construction):
    # identify inheritsFrom links
    for linkedCX in g.objects(mainCX, links.inheritedBy):
        g.add((linkedCX, links.inheritsFrom, mainCX))

# List of all symmetrical links
properties_to_mirror = ("sameFormSameFunction", "sameFormSimilarFunction", "sameFormDifferentFunction",
                        "similarFormSameFunction", "similarFormSimilarFunction", "similarFormDifferentFunction",
                        "differentFormSameFunction", "differentFormSimilarFunction", "differentFormDifferentFunction",
                        "CL_sameFormSameFunction", "CL_sameFormSimilarFunction", "CL_sameFormDifferentFunction",
                        "CL_similarFormSameFunction", "CL_similarFormSimilarFunction", "CL_similarFormDifferentFunction",
                        "CL_differentFormSameFunction", "CL_differentFormSimilarFunction", "CL_differentFormDifferentFunction"
                        )

# Add symmetrical link
for prop in properties_to_mirror:
    for subj, obj in g.subject_objects(links[prop]):
        # Add the mirrored triple
        g.add((obj, links[prop], subj))



###############################################################################
# We now distinguish between the info that should go into cx.ttl and users.ttl
###############################################################################

# Iterate over all triples in the original graph (for cx.ttl)
for s, p, o in g:
    # Check if the subject starts with the desired prefix
    if isinstance(s, URIRef) and str(s).startswith(cx):
        graph_cx.add((s, p, o))

# Serialize the filtered graph
graph_cx.serialize(destination=output_cx, format="turtle")
print(f"RDF saved to {output_cx}")

# Iterate over all triples in the original graph (for users.ttl)
for s, p, o in g:
    # Check if the subject starts with the desired prefix
    if isinstance(s, URIRef) and str(s).startswith(membr):
        graph_membr.add((s, p, o))

# Serialize the filtered graph
graph_membr.serialize(destination=output_membr, format="turtle")
print(f"RDF saved to {output_membr}")

