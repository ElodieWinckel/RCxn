from . import app_entries_blueprint
import glob
import re
from flask import Flask, render_template, redirect, url_for
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import os

# Check if the production directory exists (otherwise, defaults to development directory)
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path

g = Graph()

# The following is for debug purposes: Check for matching files
#matching_files = glob.glob("instance/Submissions/*4546_cx.ttl")
#print("Matching files:", matching_files)

# Load and parse all RDF files ending in "_cx.ttl" from the folder with submissions
for ttl_file in glob.glob("instance/Submissions/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Load and parse all RDF files in the Abox
for ttl_file in glob.glob("Abox/*.ttl"):
    g.parse(ttl_file, format="turtle")

# The following is for debug purposes: Read triples
#for s, p, o in g:
    #print(s, p, o)

# Define the namespaces
CX = Namespace("http://example.org/cx/")
g.bind("cx", CX)
olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
g.bind("rcxn", rcxn)
rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
g.bind("rsrch", rsrch)
lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
g.bind("lg", lg)

# Load the ontologies
ont = Graph()
for xlm_file in glob.glob("ontologies/*.rdf"):
    ont.parse(xlm_file, format="xml")

def get_metalanguage(lang_uri, graph, is_variety_of):
    """
    Walks up the isVarietyOf chain until it finds
    the top-level 'metalanguage' (no parent).
    """
    current = lang_uri
    visited = set()  # to avoid infinite loops if bad data
    while True:
        parents = list(graph.objects(subject=current, predicate=is_variety_of))
        if not parents:
            # no further parent, return current as the metalanguage
            return current
        parent = parents[0]
        if parent in visited:
            # cycle detected
            return current
        visited.add(parent)
        current = parent

@app_entries_blueprint.route("/")
def list_view():
    constructions = []

    # SPARQL query to get the title for each construction
    query = """
    PREFIX rcxn: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#>
    PREFIX lg: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#>
    SELECT ?construction ?title ?language
    WHERE {
        ?construction a rcxn:Construction .
        ?construction rcxn:hasTitle ?title .
        ?construction lg:partOfLanguage ?language .
    }
    """

    # Execute the SPARQL query
    results = g.query(query)

    # Process query results
    for row in results:
        construction_uri = str(row.construction)
        title = str(row.title)
        variety_uri = row.language
        variety = str(next(ont.objects(subject=variety_uri, predicate=RDFS.label), ""))
        metalanguage_uri = get_metalanguage(variety_uri, ont, lg.isVarietyOf)
        metalanguage_label = str(next(ont.objects(subject=metalanguage_uri, predicate=RDFS.label), ""))

        # Append construction details as dictionary
        constructions.append({
            'uri': construction_uri,
            'title': title,
            'variety': variety,
            'metalanguage': metalanguage_label
        })

    # Sorting in alphabetical order
    constructions = sorted(
        constructions,
        key=lambda x: (x['metalanguage'].lower(), x['title'].lower())
    )

    return render_template("app_entries/list.html", constructions=constructions)

@app_entries_blueprint.route('/construction/<path:uri>', endpoint='construction_detail')
def construction_detail(uri):
    # A list of prefixes that we might want to delete later from the URI
    prefixes = ("http://example.org/cx/|"
                "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links#|"
                "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#|"
                "http://example.org/users#|http://purl.org/olia/olia.owl#|"
                "http://purl.org/olia/olia-top.owl#|"
                "http://www.w3.org/2000/01/rdf-schema#|"
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#|"
                "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")

    def get_label_or_iri(term, data_graph, ont_graph):
        """Return rdfs:label from ontologies if available, else fallback."""
        if isinstance(term, Literal):
            return str(term)
        elif isinstance(term, URIRef):
            # First try ontology graph
            for label in ont_graph.objects(term, RDFS.label):
                return str(label)
            # Fallback: maybe the data graph has labels too
            for label in data_graph.objects(term, RDFS.label):
                return str(label)
            # Last resort: strip prefixes
            return re.sub(prefixes, "", str(term))
        else:
            return str(term)

    # Rebuild the full URI for the construction
    entry_uri = URIRef("http://example.org/cx/" + uri)
    # Rebuilt the full URI for the meaning of the construction
    meaning_uri = URIRef("http://example.org/cx/" + uri + "_Meaning")
    # Rebuilt the full URI for the sequence of elements / slots
    slots_uri = URIRef("http://example.org/cx/" + uri + "_slots")
    # Rebuilt the full URI for metadata
    metadata_uri = URIRef("http://example.org/cx/" + uri + "_MD")

    # List of all properties whose object should be a hyperlink
    links_properties = {"inheritsFrom", "inheritedBy",
                        "sameFormSameFunction", "sameFormSimilarFunction", "sameFormDifferentFunction",
                        "similarFormSameFunction", "similarFormSimilarFunction", "similarFormDifferentFunction",
                        "differentFormSameFunction", "differentFormSimilarFunction", "differentFormDifferentFunction",
                        "CL_sameFormSameFunction", "CL_sameFormSimilarFunction", "CL_sameFormDifferentFunction",
                        "CL_similarFormSameFunction", "CL_similarFormSimilarFunction", "CL_similarFormDifferentFunction",
                        "CL_differentFormSameFunction", "CL_differentFormSimilarFunction", "CL_differentFormDifferentFunction"
                        }

    # Collect all triples where entry_uri is the subject
    triples = []
    for predicate, obj in g.predicate_objects(subject=entry_uri):
        if str(predicate) != str(RDF.type):
            triples.append({
                'property': get_label_or_iri(predicate, g, ont),
                'object': get_label_or_iri(obj, g, ont),
            })

    # Add triples for meaning
    for predicate, obj in g.predicate_objects(subject=meaning_uri):
        if str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            triples.append({
                'property': re.sub(prefixes, "", str(predicate)),
                'object': re.sub(prefixes, "", str(obj)),
            })
    triples[:] = [item for item in triples if item['property'] != "hasConstructionMeaning"]
    triples[:] = [item for item in triples if item['property'] != "hasSlots"]
    triples[:] = [item for item in triples if item['property'] != "hasExample"]
    triples[:] = [item for item in triples if item['property'] != "hasMetadata"]
    triples[:] = [item for item in triples if item['property'] != "hasTitle"]

    # Separate into General and Links
    links_no_titles = [item for item in triples if item['property'] in links_properties]
    general = [item for item in triples if item['property'] not in links_properties]

    # Collect the title of links
    links = []
    title_uri = "hasTitle"
    for link in links_no_titles:
        predicate = link['property']
        object_value = link['object']
        uri = URIRef(f"http://example.org/cx/{object_value}")
        for obj in g.objects(subject=uri, predicate=URIRef(f"https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#{title_uri}")):
            links.append({
                'property': re.sub(prefixes, "", predicate),  # Cleaned property
                'object': re.sub(prefixes, "", str(obj)),  # Cleaned object
            })

    # Collect triples for elements / slots
    # Step 1: Extract the elements of the sequence
    unique_slot_uri = []
    for predicate, obj in g.predicate_objects(subject=slots_uri):
        if predicate.startswith(str(RDF)) and predicate[len(str(RDF))] == "_":  # Check for rdf:_n
            unique_slot_uri.append(obj)
    # Step 2: Collect triples where each sequence member is the subject
    elements = []
    for slot_uri in unique_slot_uri:
        for predicate, obj in g.predicate_objects(subject=slot_uri):
            if str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                elements.append({
                    'subject': re.sub(prefixes, "", str(slot_uri)),
                    'property': re.sub(prefixes, "", str(predicate)),
                    'object': re.sub(prefixes, "", str(obj)),
                })
            else: # special case for type mandatory/optional slot
                elements.append({
                    'subject': re.sub(prefixes, "", str(slot_uri)),
                    'property': "Optionality",
                    'object': re.sub(prefixes, "", str(obj)),
                })
        # Step 3: Collect triples for form of each sequence member
        subject_slotform = URIRef(str(slot_uri) + "_Form")
        for predicate, obj in g.predicate_objects(subject=subject_slotform):
            if str(predicate) == "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasSyntacticForm":  # special case for syntactic form that should be displayed as a link
                title = g.value(obj, rcxn.hasTitle)
                elements.append({
                    'subject': re.sub(prefixes, "", str(slot_uri)),
                    'property': re.sub(prefixes, "", str(predicate)),
                    'object': re.sub(prefixes, "", str(title)),
                    'href': re.sub(prefixes, "", str(obj)),
                })
            else:
                elements.append({
                    'subject': re.sub(prefixes, "", str(slot_uri)),
                    'property': re.sub(prefixes, "", str(predicate)),
                    'object': re.sub(prefixes, "", str(obj)),
                })

        # Step 4: Collect triples for index of each sequence member
        subject_index = URIRef(str(slot_uri) + "_Index")
        for predicate, obj in g.predicate_objects(subject=subject_index):
            elements.append({
                'subject': re.sub(prefixes, "", str(slot_uri)),
                'property': re.sub(prefixes, "", str(predicate)),
                'object': re.sub(prefixes, "", str(obj)),
            })
    # Step 5: Delete functional URIs
    elements[:] = [item for item in elements if item['property'] != "hasSlotForm"]
    elements[:] = [item for item in elements if item['property'] != "hasIndex"]
    elements[:] = [item for item in elements if item['property'] != "type"]


    # Collect triples for examples
    # Step 1: Extract the examples
    examples_uri = []
    for predicate, obj in g.predicate_objects(subject=entry_uri):
        if predicate.endswith("hasExample"):
            examples_uri.append(obj)
    # Step 2: Collect triples associated with example
    examples = []
    for example in examples_uri:
        for predicate, obj in g.predicate_objects(subject=example):
            if str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                examples.append({
                    'subject': re.sub(prefixes, "", str(example)),
                    'property': re.sub(prefixes, "", str(predicate)),
                    'object': re.sub(prefixes, "", str(obj)),
                })
    # Step 3: Sort the properties to have the text first
    examples = sorted(examples, key=lambda x: {key: index for index, key in enumerate(['hasText', 'hasTransliteration', 'hasGlosses', 'hasTranslation', 'comment'])}.get(x['property'], 5))
    # Step 3: Group by example
    grouped_examples = {}
    for item in examples:
        subject = item['subject']
        if subject not in grouped_examples:
            grouped_examples[subject] = []
        grouped_examples[subject].append({'property': item['property'], 'object': item['object']})

    # Collect triples for metadata
    metadata = []
    for predicate, obj in g.predicate_objects(subject=metadata_uri):
        if str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            metadata.append({
                'property': re.sub(prefixes, "", str(predicate)),
                'object': re.sub(prefixes, "", str(obj)),
            })

    # Collect triples for research question and findings
    research = []
    for finding in g.subjects(RDF.type, rsrch.Finding):
        # Check for the triple with form (X, rsrch:basedOn, entry_uri)
        if (finding, rsrch.basedOn, entry_uri) in g:
            # Get the rdfs:label for this finding
            finding_labels = g.objects(finding, RDFS.label)
            for finding_label in finding_labels:
                research.append({'property': 'Findings', 'object': str(finding_label)})
            # Next, query all URIs that correspond to this finding
            for project in g.subjects(rsrch.hasFindings, finding):
                project_names = g.objects(project, rsrch.projectName)
                for project_name in project_names:
                    research.append({'property': 'Research Question', 'object': str(project_name)})
    # Sorting the list so that 'Research Question' comes before 'Findings'
    research.sort(key=lambda x: x['property'], reverse=True)

    # Fetch the title to display
    title = g.value(entry_uri, rcxn.hasTitle)

    return render_template("app_entries/construction.html",
                           title=title,
                           triples=general,
                           elements=elements,
                           grouped_examples=grouped_examples,
                           links=links,
                           metadata=metadata,
                           research=research)

