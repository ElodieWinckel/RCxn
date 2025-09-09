from rdflib import Graph, Namespace
import glob

# File paths
input_file = "instance/Submissions/FernandezSantos_20241125_105826_cx.ttl"
output_file = "instance/Submissions/test_cx.ttl"

# Load RDF graph
g = Graph()
for ttl_file in glob.glob("instance/Submissions/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Namespaces
cx = Namespace("http://example.org/cx/")
g.bind("cx", cx)

membr = Namespace("http://example.org/users#")
g.bind("membr", membr)

RCXN = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
g.bind("rcxn", RCXN)

rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
g.bind("rsrch", rsrch)

links = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links#")
g.bind("links", links)

foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.bind("foaf", foaf)

olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)

oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
g.bind("oliatop", oliatop)

RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
g.bind("RDFS", RDFS)

lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
g.bind("lg", lg)

RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")


# If some construction uses another construction as construction element, then link back the second construction to the first one
for construction in g.subjects(RDF_NS.type, RCXN.Construction):
    # Get the sequence of slots
    for sequence in g.objects(construction, RCXN.hasSlots):
        # RDF collections are often numbered rdf:_1, rdf:_2, etc.
        for slot_pred, slot in g.predicate_objects(sequence):
            if str(slot_pred).startswith(str(RDF_NS["_"])):
                # Get the slot form
                for form in g.objects(slot, RCXN.hasSlotForm):
                    # Get the syntactic form (part)
                    for part in g.objects(form, RCXN.hasSyntacticForm):
                        # Add new triple: ?part rcxn:elementOf ?construction
                        g.add((part, RCXN.elementOf, construction))

for mainCX in g.subjects(RDF_NS.type, RCXN.Construction):
    # identify inheritsFrom links
    for linkedCX in g.objects(mainCX, links.inheritsFrom):
        g.add((linkedCX, links.inheritedBy, mainCX))

for mainCX in g.subjects(RDF_NS.type, RCXN.Construction):
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

# Save the updated graph
g.serialize(destination=output_file, format="turtle")

print(f"Updated RDF saved to {output_file}")