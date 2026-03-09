from . import app_compcon_blueprint
import glob
import re
from flask import render_template, Response
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, FOAF, SKOS
import os

###################################################
### FUNCTIONS
###################################################

prefixes = "https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#"

def get_label_or_iri(term, data_graph, ont_graph):
    """Return skos:prefLabel or rdfs:label from ontologies if available."""
    if isinstance(term, Literal):
        return str(term)
    elif isinstance(term, URIRef):
        # First try ontology graph with preflabel
        for label in ont_graph.objects(term, SKOS.prefLabel):
            return str(label)
        # Then try ontology graph with label
        for label in ont_graph.objects(term, RDFS.label):
            return str(label)
        # Fallback: maybe the data graph has labels too
        for label in data_graph.objects(term, RDFS.label):
            return str(label)
        # Last resort: strip prefixes
        return re.sub(prefixes, "", str(term))
    else:
        return str(term)

def get_definition(term, data_graph, ont_graph):
    """Return rdfs:comment from ontologies if available."""
    if isinstance(term, Literal):
        return str("")
    elif isinstance(term, URIRef):
        # Keep only the text, getting rid of html code <a>, </i> etc.
        for definition in ont_graph.objects(term, RDFS.comment):
            return re.sub(r'<[^>]+>', '', str(definition))
        # Fallback: maybe the data graph has labels too
        for definition in data_graph.objects(term, RDFS.comment):
            return re.sub(r'<[^>]+>', '', str(definition))
        # Last resort: empty string
        return str("")
    else:
        return str("")

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

# Define the namespaces
compcon = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#")
g.bind("compcon", compcon)

# Load the ontology (only compcon needed)
ont = Graph()
for ttl_file in glob.glob("ontologies/*.ttl"): # for compcon
    ont.parse(ttl_file, format="turtle")

###################################################
### CREATE A LIST OF CONSTRUCTIONS
###################################################

@app_compcon_blueprint.route("/")
def list_view():
    list_of_sem = []

    for cc in ont.subjects(predicate=RDF.type, object=compcon.sem):
        compcon_uri = str(cc)
        title = str(ont.value(subject=cc, predicate=RDFS.label))

        # Append construction details as dictionary
        list_of_sem.append({
            'uri': compcon_uri,
            'title': title
        })

    # Sorting in alphabetical order
    list_of_sem = sorted(
        list_of_sem,
        key=lambda x: (x['title'].lower())
    )

    return render_template("app_compcon/list.html", list_of_sem=list_of_sem)

###################################################
### CREATE CONSTRUCTION ENTRIES
###################################################

@app_compcon_blueprint.route('/entry/<path:uri>', endpoint='comparative_concept_detail')
def comparative_concept_detail(uri):

    # Rebuild the full URI for the construction
    entry_uri = URIRef("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#" + uri)

    # Collect all triples from the ontology where entry_uri is the subject
    description = []
    for predicate, obj in ont.predicate_objects(subject=entry_uri):
        description.append({
            'property': get_label_or_iri(predicate, g, ont),
            'object': get_label_or_iri(obj, g, ont)
        })

    # Collect all triples from the A-box where entry_uri is the subject
    for predicate, obj in g.predicate_objects(subject=entry_uri):
        description.append({
            'property': get_label_or_iri(predicate, g, ont),
            'object': get_label_or_iri(obj, g, ont)
        })

    # Fetch the title to display
#    title = g.value(entry_uri, rcxn.hasTitle)

    return render_template("app_compcon/entry.html",
                           description = description)