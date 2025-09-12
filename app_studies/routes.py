from jinja2.utils import Namespace

from . import app_studies_blueprint
import glob
import re
from flask import Flask, render_template, redirect, url_for
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import os

# Check if the production directory exists (otherwise, defaults to development directory)
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path

g = Graph()

# Load and parse all RDF files from the folder with submissions
for ttl_file in glob.glob("instance/Submissions/*.ttl"):
    g.parse(ttl_file, format="turtle")

# Load and parse all RDF files in the Abox
for ttl_file in glob.glob("Abox/*.ttl"):
    g.parse(ttl_file, format="turtle")

# Define the namespaces
CX = Namespace("http://example.org/cx/")
g.bind("cx", CX)
olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
dc = Namespace("http://purl.org/dc/elements/1.1/")
g.bind("dc",dc)
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

@app_studies_blueprint.route("/")
def studies_view():
    studies = []

    # SPARQL query to get the title for each study
    query = """
    PREFIX rdata: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#>
    SELECT ?study ?title ?type
    WHERE {
        ?study a rdata:Study .
        ?study rdata:hasTitle ?title .
        ?study rdata:studyType ?type .
    }
    """

    # Execute the SPARQL query
    results = g.query(query)

    # Process query results
    for row in results:
        study_uri = str(row.study)
        title = str(row.title)
        type = str(row.type)

        # Append study details as dictionary
        studies.append({
            'uri': study_uri,
            'title': title,
            'type': re.sub("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#","",type)
        })

    # Sorting in alphabetical order
    studies = sorted(
        studies,
        key=lambda x: (x['title'].lower())
    )

    return render_template("app_studies/list.html", studies=studies)

@app_studies_blueprint.route('/study/<path:uri>', endpoint='study_detail')
def study_detail(uri):
    # A list of prefixes that we might want to delete later from the URI
    prefixes = ("http://example.org/cx/|"
                "http://example.org/rd/|"
                "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links#|"
                "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#|"
                "http://example.org/users#|http://purl.org/olia/olia.owl#|"
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

    # Rebuild the full URI for the construction
    study_uri = URIRef("http://example.org/rd/" + uri)

    # Collect all triples where entry_uri is the subject
    triples = []
    for predicate, obj in g.predicate_objects(subject=study_uri):
        if str(predicate) != str(RDF.type):
            triples.append({
                'property': get_label_or_iri(predicate, g, ont),
                'object': get_label_or_iri(obj, g, ont),
            })
    triples[:] = [item for item in triples if item['property'] != "hasTitle"]
    triples[:] = [item for item in triples if item['property'] != "dataRepository"]
    triples[:] = [item for item in triples if item['property'] != "relevantFor"]
    triples[:] = [item for item in triples if item['property'] != "Visualization"]
    triples[:] = [item for item in triples if item['property'] != "publishedIn"]

    # collect references
    references = []
    for collection in g.objects(subject=study_uri, predicate=rdata.publishedIn):
            # Get all literature entries in this collection
            for lit in g.objects(collection, CX.hasLiterature):
                # Extract details for each literature entry
                creators = [str(c) for c in g.objects(lit, dc.creator)]
                date = g.value(lit, dc.date)
                title = g.value(lit, dc.title)
                identifier = g.value(lit, dc.identifier)
                # Format authors as "Last1, Last2 & Last3"
                authors = []
                for creator in creators:
                    last_name = creator.split(", ")[0]
                    authors.append(last_name)
                authors_str = " & ".join([", ".join(authors[:-1])] + [authors[-1]] if len(authors) > 2 else authors)
                doi_str=str(identifier).replace("DOI ", "")
                doi_href="https://www.doi.org/"+doi_str
                references.append({
                    "authors": authors_str,
                    "year": str(date),
                    "title": str(title),
                    "doi": doi_str,
                    "doi_href": doi_href
                })

    for obj in g.objects(subject=study_uri, predicate=rdata.dataRepository):
        triples.append({
            'property': "dataRepository",
            'object': get_label_or_iri(obj, g, ont),
            'href': get_label_or_iri(obj, g, ont)
        })

    for obj in g.objects(subject=study_uri, predicate=rdata.relevantFor):
        href = "../../app_entries/construction/" + re.sub(prefixes, "", get_label_or_iri(obj, g, ont))
        title = g.value(obj, rcxn.hasTitle)
        triples.append({
            'property': "relevantFor",
            'object': title,
            'href': href
        })

    figures = []
    for figure in g.objects(subject=study_uri, predicate=rdata.Visualization):
        path = "Research_data/" + get_label_or_iri(figure, g, ont) + ".png"
        description = g.value(subject=figure, predicate=dc.description)
        title = g.value(subject=figure, predicate=dc.title)
        figures.append({
            'path': path,
            'description': description,
            'title': title,
        })


    # Fetch the title to display
    title = g.value(study_uri, rdata.hasTitle)

    return render_template("app_studies/study.html",
                           title=title,
                           triples=triples,
                           figures=figures,
                           references=references)

