from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, RDF
import re
import glob

# File paths
output_cx = "Abox/cx.ttl"
output_membr = "Abox/membr.ttl"
output_references = "Abox/references.ttl"

# Create general graph, and subgraphs holders for cx, membr and references
g = Graph()
graph_cx = Graph()
graph_membr = Graph()
graph_references = Graph()

# Load everything from the submissions (assuming that everything in the submission folder has now a green light)
for ttl_file in glob.glob("instance/Submissions/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Namespaces
cx = Namespace("http://example.org/cx/")
g.bind("cx", cx)
graph_cx.bind("cx", cx)
graph_membr.bind("cx", cx)

membr = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/Abox/membr#")
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
def add_user(last_name, first_name, project_name, homepage):
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
    # related to researcher
    g.add((user_uri, RDF.type, FOAF.Person))
    g.add((user_uri, FOAF.familyName, Literal(last_name)))
    g.add((user_uri, FOAF.givenName, Literal(first_name)))
    g.add((user_uri, FOAF.currentProject, project_uri))
    g.add((user_uri, FOAF.homepage, URIRef(homepage)))
    # related to projects
    g.add((project_uri, RDF.type, rsrch.Project))
    g.add((project_uri, rsrch.projectName, Literal(project_name, lang = "en")))

# Add RTG members to the graph
add_user("Alhabyan",
         "Raghad",
         "Valency, preposition governing, and phrasal verbs in Arabic and Semitic",
         "https://www.cxg.phil.fau.eu/person/raghad-alhabyan/")
add_user("Badawi",
         "Soran",
         "Corpus-based measures of constructionhood",
         "https://www.cxg.phil.fau.eu/person/soran-badawi/")
add_user("Bayer",
         "Nadine",
         "Project Bayer",
         "https://www.cxg.phil.fau.eu/person/nadine-bayer/")
add_user("Benito Fernandez",
         "Elba",
         "Spanish quotative constructions in oral narratives — an Interactional Construction Grammar approach",
         "https://www.cxg.phil.fau.eu/person/elba-benito-fernandez/")
add_user("Blake",
         "Ashley",
         "Project Blake",
         "https://www.cxg.phil.fau.eu/person/ashley-blake/")
add_user("Boos",
         "Julia",
         "Entrenchment meets literacy: How the development of reading ability affects child and adult language processing",
         "https://www.cxg.phil.fau.eu/person/julia-boos/")
add_user("De la Garza",
         "Vania",
         "Project De la Garza",
         "https://www.cxg.phil.fau.eu/person/vania-de-la-garza/")
add_user("Fernández Santos",
         "Sara",
         "Artificial language learning as a window to the early entrenchment of constructions",
         "https://www.cxg.phil.fau.eu/person/vania-de-la-garza/")
add_user("Fokashchuk",
         "Iryna",
         "Functions and cognitive semantics of prepositions in complex constructions",
         "https://www.cxg.phil.fau.eu/person/iryna-fokashchuk/")
add_user("Führer",
         "Bastian",
         "German verbs with particles or prefixes in language change: Form, meaning, and syntax",
         "https://www.cxg.phil.fau.eu/person/bastian-fuhrer/")
add_user("Gedik",
         "Tan Arda",
         "Project Gedik",
         "https://www.cxg.phil.fau.eu/person/tan-arda-gedik/")
add_user("Gromadsky",
         "Dmitry",
         "Constructions in communication",
         "https://www.cxg.phil.fau.eu/person/dmitry-gromadsky/")
add_user("Grose-Hodge",
         "Magdalena",
         "Project Grose-Hodge",
         "https://www.cxg.phil.fau.eu/person/magdalena-grose-hodge/")
add_user("Hutta",
         "Sophie",
         "Project Hutta",
         "https://www.cxg.phil.fau.eu/person/sophie-hutta/")
add_user("Iabdounane",
         "Yassine",
         "Multimodal constructional space",
         "https://www.cxg.phil.fau.eu/person/yassine-iabdounane/")
add_user("Immertreu",
         "Mathis",
         "Multimodal cognitive maps for cross-domain constructional networks",
         "https://www.cxg.phil.fau.eu/person/mathis-immertreu/")
add_user("Kashigin",
         "Kyra",
         "Contrastive Construction Grammar: The interaction of argument-structure constructions and sentence-type constructions in english, Dutch and German",
         "https://www.cxg.phil.fau.eu/person/kyra-kashigin/")
add_user("Kassler",
         "Annika",
         "Project Kassler",
         "https://www.cxg.phil.fau.eu/person/annika-kassler/")
add_user("Kenanidis",
         "Panagiotis",
         "Project Kenanidis",
         "https://www.cxg.phil.fau.eu/person/panagiotis-kenanidis/")
add_user("Keßler",
         "Florian",
         "Chinese Mathematics",
         "https://www.cxg.phil.fau.eu/person/florian-kesler/")
add_user("Khanoub",
         "Rania",
         "Project Khanoub",
         "https://www.cxg.phil.fau.eu/person/rania-khanoub/")
add_user("Kissane",
         "Hassane",
         "Form and meaning as factors in the identification and learning of constructional slots – English phrasal verbs and verb-preposition combinations",
         "https://www.cxg.phil.fau.eu/person/hassane-kissane/")
add_user("Kligge",
         "Hendrik",
         "Representation and acquisition of agreement relations in a usage-based framework",
         "https://www.cxg.phil.fau.eu/person/hendrik-kligge/")
add_user("Lee",
         "Dongeun",
         "Project Lee",
         "https://www.cxg.phil.fau.eu/person/dongeun-lee/")
add_user("Makhanina",
         "Asia",
         "Representation and acquisition of idiomatic constructions in L1 and L2 learners",
         "https://www.cxg.phil.fau.eu/person/asia-makhanina/")
add_user("Patel",
         "Malin",
         "Corpus evidence for delineating constructions",
         "https://www.cxg.phil.fau.eu/person/malin-patel/")
add_user("Petrenko",
         "Elizaveta",
         "Comparing constructions cross-linguistically — Connecting constructicons",
         "https://www.cxg.phil.fau.eu/person/elizaveta-petrenko/")
add_user("Prela",
         "Leonarda",
         "Project Prela",
         "https://www.cxg.phil.fau.eu/person/leonarda-prela/")
add_user("Ramezani",
         "Pegah",
         "Representation and processing of constructions in the brain",
         "https://www.cxg.phil.fau.eu/person/pegah-ramezani/")
add_user("Rastegar",
         "Aria",
         "Representation and acquisition of idiomatic constructions in L1 and L2 learners",
         "https://www.cxg.phil.fau.eu/person/aria-rastegar/")
add_user("Rohwedder",
         "Paul",
         "Project Rohwedder",
         "https://www.cxg.phil.fau.eu/person/paul-rohwedder/")
add_user("Legouté",
         "Anne Sherley",
         "Multifunctionality in Haitian Creole: New insights from a Construction Grammar perspective",
         "https://www.cxg.phil.fau.eu/person/anne-sherley-legoute/")
add_user("Schmechel",
         "Dennis",
         "Project Schmechel",
         "https://www.cxg.phil.fau.eu/person/dennis-schmechel/")
add_user("Senger",
         "Lena",
         "Project Senger",
         "https://www.cxg.phil.fau.eu/person/lena-senger/")
add_user("Stampfer",
         "Veronika",
         "Semantically related argument structures in the history of English",
         "https://www.cxg.phil.fau.eu/person/veronika-stampfer/")
add_user("Trombetta",
         "Chiara",
         "Constructions beyond the sentence: text-structuring in (esp.) sixteenth-century historiographical texts",
         "https://www.cxg.phil.fau.eu/person/chiara-trombetta/")
add_user("Tzimas",
         "Theocharis",
         "Subject-inversion throughout Early Modern English: changing relations in individual and communal constructions",
         "https://www.cxg.phil.fau.eu/person/theocharis-tzimas/")
add_user("Wright",
         "Richenda",
         "Project Wright",
         "https://www.cxg.phil.fau.eu/person/richenda-wright/")
add_user("Weigelt",
         "Lina",
         "Project Weigelt",
         "https://www.cxg.phil.fau.eu/person/lina-weigelt/")
add_user("Winckel",
         "Elodie",
         "Building a Research Constructicon",
         "https://www.cxg.phil.fau.eu/person/elodie-winckel/")

# If some construction uses another construction as construction element, then link back the second construction to the first one
for subj, part in g.subject_objects(rcxn.hasSyntacticForm):
    # identify the IRI of the construction
    construction_uri = re.sub(r'_\d+_Form$', '', subj)
    # Add new triple: ?part rcxn:elementOf ?construction
    g.add((part, rcxn.elementOf, URIRef(construction_uri)))

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

# If construction A has a metaphorical extension B, then B is a metaphorical extension of A
for subj, obj in g.subject_objects(links.metaphoricalLink):
        g.add((obj, links.isMetaphoricalExtensionOf, subj))
###############################################################################
# We now distinguish between the IRI that belong to cx.ttl, membr.ttl and references.ttl
###############################################################################

# Iterate over all triples in the original graph (for cx.ttl)
for s, p, o in g:
    # Check if the subject starts with the desired prefix
    if isinstance(s, URIRef) and str(s).startswith(cx):
        graph_cx.add((s, p, o))

# Serialize the filtered graph
graph_cx.serialize(destination=output_cx, format="turtle")
print(f"RDF saved to {output_cx}")

# Iterate over all triples in the original graph (for membr.ttl)
for s, p, o in g:
    # Check if the subject starts with the desired prefix
    if isinstance(s, URIRef) and str(s).startswith(membr):
        graph_membr.add((s, p, o))

# Serialize the filtered graph
graph_membr.serialize(destination=output_membr, format="turtle")
print(f"RDF saved to {output_membr}")

# Identify references and save them in a dedicated A-box
for subject, reference in g.subject_objects(cx.hasLiterature):
    for p, o in g.predicate_objects(reference):
        graph_references.add((reference, p, o))
# Serialize the filtered graph
graph_references.serialize(destination=output_references, format="turtle")
print(f"RDF saved to {output_references}")