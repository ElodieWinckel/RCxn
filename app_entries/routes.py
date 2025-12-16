from . import app_entries_blueprint
import glob
import re
from flask import Flask, render_template, Response
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, FOAF
import os
from io import BytesIO

###################################################
### FUNCTIONS
###################################################

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

# A list of prefixes that we might want to delete later from the URI
prefixes = ("http://example.org/cx/|"
            "http://example.org/rd/|"
            "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links-1.1#|"
            "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#|"
            "https://bdlweb.phil.uni-erlangen.de/RCxn/Abox/membr#|"
            "http://purl.org/olia/olia.owl#|"
            "http://purl.org/olia/olia-top.owl#|"
            "http://www.w3.org/2000/01/rdf-schema#|"
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#|"
            "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#|"
            "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#")

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

def identify_construction_element_triples(slots_uri):
    # Step 1: Extract the elements of the sequence
    unique_slot_uri = []
    for predicate, obj in g.predicate_objects(subject=slots_uri):
        if predicate.startswith(str(RDF)) and predicate[len(str(RDF))] == "_":  # Check for rdf:_n
            unique_slot_uri.append(obj)
    # Step 2: Identify the sequence members that have slots
    list_of_nested = []
    for slot_uri in unique_slot_uri:
        for predicate, obj in g.predicate_objects(subject=slot_uri):
            if str(predicate) == "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasSlots":
                list_of_nested.append(str(slot_uri))
    # Step 2: Collect triples where each sequence member is the subject
    elements = []
    colloprofiles = []
    for slot_uri in unique_slot_uri:
        # Define the name of the slot
        element_number = "Element " + slot_uri[-1]
        # Extract colloprofiles for this slot
        collo = []
        for collo_list in g.objects(subject=slot_uri, predicate=cx.colloprofile):
            for item in g.items(collo_list):
                word = g.value(item, cx.word)
                freq = g.value(item, cx.frequency)
                collo.append({"word": str(word), "frequency": int(freq)})
        if collo:  # append only if there is a colloprofile
            collo.sort(key=lambda x: x["frequency"], reverse=True)  # Sort by frequency (descending)
            colloprofiles.append({
                "subject_name": element_number,
                "collocations": collo
            })
        # Gather triplets
        for predicate, obj in g.predicate_objects(subject=slot_uri):
            if str(predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":  # special case for type mandatory/optional slot
                elements.append({
                    'subject': element_number,
                    'property': "Optionality",
                    'object': get_label_or_iri(obj, g, ont),
                })
            else:
                if str(predicate) == "http://example.org/cx/colloprofile":  # special case for colloprofile
                    elements.append({
                        'subject': element_number,
                        'property': "Colloprofile",
                        'object': "See colloprofile for " + element_number + " below",
                    })
                else:  # all other cases
                    elements.append({
                        'subject': element_number,
                        'property': get_label_or_iri(predicate, g, ont),
                        'object': get_label_or_iri(obj, g, ont),
                    })

        # Step 3: Collect triples for form of each sequence member
        subject_slotform = URIRef(str(slot_uri) + "_Form")
        for predicate, obj in g.predicate_objects(subject=subject_slotform):
            if str(predicate) == "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasSyntacticForm":  # special case for syntactic form that should be displayed as a link
                title = g.value(obj, rcxn.hasTitle)
                elements.append({
                    'subject': element_number,
                    'property': get_label_or_iri(predicate, g, ont),
                    'object': get_label_or_iri(title, g, ont),
                    'href': get_label_or_iri(obj, g, ont),
                })
            else:
                elements.append({
                    'subject': element_number,
                    'property': get_label_or_iri(predicate, g, ont),
                    'object': get_label_or_iri(obj, g, ont),
                })

        # Step 4: Collect triples for index of each sequence member
        subject_index = URIRef(str(slot_uri) + "_Index")
        for predicate, obj in g.predicate_objects(subject=subject_index):
            elements.append({
                'subject': element_number,
                'property': get_label_or_iri(predicate, g, ont),
                'object': get_label_or_iri(obj, g, ont),
            })
    elements[:] = [item for item in elements if item['property'] != "type"]
    elements[:] = [item for item in elements if item['property'] != "hasSlotForm"]
    elements[:] = [item for item in elements if item['property'] != "hasIndex"]
    return elements, colloprofiles, list_of_nested


###################################################
### CREATE RDF GRAPH
###################################################

g = Graph()

# Check if the production directory exists (otherwise, defaults to development directory)
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path

else:
    # Load and parse all RDF files from the folder with submissions (only during development process)
    for ttl_file in glob.glob("instance/Submissions/*.ttl"):
        g.parse(ttl_file, format="turtle")

# Load and parse all RDF files in the Abox
for ttl_file in glob.glob("Abox/*.ttl"):
    g.parse(ttl_file, format="turtle")

# The following is for debug purposes: Read triples
#for s, p, o in g:
    #print(s, p, o)

# Define the namespaces
cx = Namespace("http://example.org/cx/")
g.bind("cx", cx)
dc = Namespace("http://purl.org/dc/elements/1.1/")
g.bind("dc",dc)
olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
g.bind("rcxn", rcxn)
rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
g.bind("rsrch", rsrch)
lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
g.bind("lg", lg)
rd = Namespace("http://example.org/rd/") #TODO: is this really the name?
g.bind("rd", rd)
rdata = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#") #TODO: is this really the name? create ontology
g.bind("rdata", rdata)

# Load the ontologies
ont = Graph()
for xlm_file in glob.glob("ontologies/*.rdf"):
    ont.parse(xlm_file, format="xml")
for xlm_file in glob.glob("ontologies/*.owl"):
    ont.parse(xlm_file, format="xml")

###################################################
### CREATE A LIST OF CONSTRUCTIONS
###################################################

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

###################################################
### CREATE CONSTRUCTION ENTRIES
###################################################

@app_entries_blueprint.route('/construction/<path:uri>', endpoint='construction_detail')
def construction_detail(uri):

    # Rebuild the full URI for the construction
    entry_uri = URIRef("http://example.org/cx/" + uri)
    # Rebuilt the full URI for the meaning of the construction
    meaning_uri = URIRef("http://example.org/cx/" + uri + "_Meaning")
    # Rebuilt the full URI for the sequence of elements / slots
    slots_uri = URIRef("http://example.org/cx/" + uri + "_slots")
    # Rebuilt the full URI for metadata
    metadata_uri = URIRef("http://example.org/cx/" + uri + "_MD")

    # Collect all triples where entry_uri is the subject
    triples = []
    links = []
    for predicate, obj in g.predicate_objects(subject=entry_uri):
        if str(predicate) != str(RDF.type):
            if str(predicate).startswith("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links-1.1#"):
                name_of_link = get_label_or_iri(predicate, g, ont)
                object_value = get_label_or_iri(obj, g, ont)
                uri = URIRef(f"http://example.org/cx/{object_value}")
                for title in g.objects(subject=uri, predicate=rcxn.hasTitle):
                    lang_uri = g.value(subject=uri, predicate=lg.partOfLanguage)
                    links.append({
                        'property': name_of_link,
                        'object': get_label_or_iri(title, g, ont),
                        'href': object_value,
                        'lang': get_label_or_iri(lang_uri, g, ont),
                    })
            else:
                if str(predicate).endswith("elementOf"): # Special case for "eelement of", which is not part of the ontology of links
                    name_of_link = get_label_or_iri(predicate, g, ont)
                    object_value = get_label_or_iri(obj, g, ont)
                    uri = URIRef(f"http://example.org/cx/{object_value}")
                    for title in g.objects(subject=uri, predicate=rcxn.hasTitle):
                        lang_uri = g.value(subject=uri, predicate=lg.partOfLanguage)
                        links.append({
                            'property': name_of_link,
                            'object': get_label_or_iri(title, g, ont),
                            'href': object_value,
                            'lang': get_label_or_iri(lang_uri, g, ont),
                        })
                else:
                    triples.append({
                        'property': get_label_or_iri(predicate, g, ont),
                        'object': get_label_or_iri(obj, g, ont),
                    })

    # Add triples for meaning
    for predicate, obj in g.predicate_objects(subject=meaning_uri):
        if str(predicate) == "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasMeaning":
            meaning_text = re.sub(prefixes, "", str(obj))
            html_code = re.sub(r'\[([^\]]*)\](\d+)', r'<ce\2>\1</ce\2>', meaning_text)
            triples.append({
                'property': "Meaning of the construction",
                'object': html_code,
            })
        else:
            if str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                triples.append({
                    'property': get_label_or_iri(predicate, g, ont),
                    'object': get_label_or_iri(obj, g, ont),
                })

    triples[:] = [item for item in triples if item['property'] != "hasConstructionMeaning"]
    triples[:] = [item for item in triples if item['property'] != "hasSlots"]
    triples[:] = [item for item in triples if item['property'] != "hasExample"]
    triples[:] = [item for item in triples if item['property'] != "hasMetadata"]
    triples[:] = [item for item in triples if item['property'] != "Title"]
    triples[:] = [item for item in triples if item['property'] != "basedOnStudy"]

    # Collect triples for elements / slots
    elements, colloprofiles, list_of_nested = identify_construction_element_triples(slots_uri)
    for nested in list_of_nested:
        slot_uri_nested = URIRef(nested + "_slots")
        nested_elements, nested_colloprofiles, nested_list_of_nested = identify_construction_element_triples(slot_uri_nested)
        # Define the name of the slot
        element_number = "Element " + nested[-1]
        elements.append({
            'subject': str(element_number),
            'children': nested_elements
        })


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
            if str(predicate) == "http://example.org/cx/hasAnnotatedText":
                example_text = re.sub(prefixes, "", str(obj))
                html_code = re.sub(r'\[([^\]]*)\](\d+)', r'<ce\2>\1</ce\2>', example_text)
                examples.append({
                    'subject': re.sub(prefixes, "", str(example)),
                    'property': "Text",
                    'object': html_code,
                })
            else:
                examples.append({
                    'subject': re.sub(prefixes, "", str(example)),
                    'property': re.sub(prefixes, "", str(predicate)),
                    'object': re.sub(prefixes, "", str(obj)),
                })
    examples[:] = [item for item in examples if item['property'] != "type"]
    examples[:] = [item for item in examples if item['property'] != "hasText"]
    # Step 3: Sort the properties to have the text first
    examples = sorted(examples, key=lambda x: {key: index for index, key in enumerate(['Text', 'hasTransliteration', 'hasGlosses', 'hasTranslation', 'comment'])}.get(x['property'], 5))
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
        if str(predicate) == "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#annotator":
            given = g.value(subject=obj, predicate=FOAF.givenName)
            family = g.value(subject=obj, predicate=FOAF.familyName)
            homepage = g.value(subject=obj, predicate=FOAF.homepage)
            metadata.append({
                'property': get_label_or_iri(predicate, g, ont),
                'given': get_label_or_iri(given, g, ont),
                'family': get_label_or_iri(family, g, ont),
                'homepage': get_label_or_iri(homepage, g, ont),
            })
        elif str(predicate) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            metadata.append({
                'property': get_label_or_iri(predicate, g, ont),
                'object': get_label_or_iri(obj, g, ont),
            })
    metadata[:] = [item for item in metadata if item['property'] != "hasSources"] # resources are delt with separately (see below "collect references")

    # collect references
    references = []
    for collection in g.objects(subject=metadata_uri, predicate=cx.hasSources):
            # Get all literature entries in this collection
            for lit in g.objects(collection, cx.hasLiterature):
                # Extract details for each literature entry
                creators = [str(c) for c in g.objects(lit, dc.creator)]
                contributors = [str(c) for c in g.objects(lit, dc.contributor)]
                date = g.value(lit, dc.date)
                title = g.value(lit, dc.title)
                identifier = g.value(lit, dc.identifier)
                source = g.value(lit, dc.source)
                # Format authors as "Last1, Last2 & Last3"
                authors = []
                for creator in creators:
                    last_name = creator.split(", ")[0]
                    authors.append(last_name)
                authors_str = " & ".join([", ".join(authors[:-1])] + [authors[-1]] if len(authors) > 2 else authors)
                # Format editors as "Last1, Last2 & Last3"
                editors = []
                for contributor in contributors:
                    last_name = contributor.split(", ")[0]
                    editors.append(last_name)
                editors_str = " & ".join([", ".join(editors[:-1])] + [editors[-1]] if len(editors) > 2 else editors)
                # Add DOI if it exists
                doi_str=str(identifier).replace("DOI ", "")
                if doi_str.strip() != "None":
                    doi_href="https://www.doi.org/"+doi_str
                # Create the entry for the resource in the dictionary and append
                reference = {}
                if authors_str and authors_str.strip():
                    reference["authors"] = authors_str
                if editors_str and editors_str.strip():
                    reference["editors"] = editors_str + " (ed.)"
                if str(date).strip() != "None":
                    reference["year"] = str(date)
                if str(title).strip():
                    reference["title"] = str(title)
                if doi_str.strip() != "None":
                    reference["doi"] = doi_str
                    reference["doi_href"] = doi_href
                if str(source).strip() != "None":
                    reference["source"] = str(source)
                references.append(reference)

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

    # Collect triples for research data
    research_data = []
    for study in g.objects(entry_uri, rdata.basedOnStudy):
        title = g.value(study, rdata.hasTitle)
        type = g.value(study, rdata.studyType)
        summary = g.value(study, rdata.Summary)
        href = re.sub(prefixes, "", str(study))
        research_data.append({'title': str(title),
                              'type': re.sub(prefixes, "", str(type)),
                              'summary': str(summary),
                              'href': href})

    # Fetch the title to display
    title = g.value(entry_uri, rcxn.hasTitle)

    return render_template("app_entries/construction.html",
                           title=title,
                           triples=triples,
                           elements=elements,
                           grouped_examples=grouped_examples,
                           links=links,
                           metadata=metadata,
                           research=research,
                           research_data=research_data,
                           references=references,
                           colloprofiles=colloprofiles)

@app_entries_blueprint.route('/construction/<path:uri>/submit', methods=['POST'])
def download_subgraph(uri):
    # Rebuild the full URI for the construction
    construction = uri.replace("submit", "")
    entry_uri = URIRef("http://example.org/cx/" + construction)
    entry_metadata = URIRef("http://example.org/cx/" + construction + "_MD")

    # Define the namespaces for a subgraph
    subgraph = Graph()
    cx = Namespace("http://example.org/cx/")
    subgraph.bind("cx", cx)
    dc = Namespace("http://purl.org/dc/elements/1.1/")
    subgraph.bind("dc", dc)
    olia = Namespace("http://purl.org/olia/olia.owl#")
    subgraph.bind("olia", olia)
    rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
    subgraph.bind("rcxn", rcxn)
    rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
    subgraph.bind("rsrch", rsrch)
    lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
    subgraph.bind("lg", lg)
    rd = Namespace("http://example.org/rd/")  # TODO: is this really the name?
    subgraph.bind("rd", rd)
    rdata = Namespace(
        "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#")  # TODO: is this really the name? create ontology
    subgraph.bind("rdata", rdata)

    # Extract the subgraph
    for s, p, o in g:
        # Check if the subject starts with the uri of the construction (for all slots, etc.)
        if isinstance(s, URIRef) and str(s).startswith(entry_uri):
            subgraph.add((s, p, o))

    # Identify references and ad them to the graph
    for collection in g.objects(entry_metadata, cx.hasSources):
        for reference in g.objects(collection, cx.hasLiterature):
            for p, o in g.predicate_objects(reference):
                subgraph.add((reference, p, o))

    # Serialize the subgraph to a string
    ttl_data = subgraph.serialize(format='turtle')

    # Send the file as a response
    return Response(
        ttl_data,
        mimetype='text/turtle',
        headers={
            'Content-Disposition': f'attachment; filename=construction_{uri}.ttl'
        }
    )