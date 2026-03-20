from typing import Any
from . import app_compcon_blueprint
import glob
import re
from flask import render_template, url_for
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS, SKOS
import os

###################################################
### FUNCTIONS
###################################################

prefixes = ("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#|" +
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#|" +
            "http://www.w3.org/2004/02/skos/core#")

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

def find_compcon_url_by_label(label_compcon) -> str:
    # Identify its URI (the definition use either the label or the alternative label)
    uri_compcon = ont.value(predicate=RDFS.label, object=Literal(label_compcon))
    if uri_compcon is None:
        uri_compcon = ont.value(predicate=SKOS.altLabel, object=Literal(label_compcon))
    uri_compcon_no_prefix = re.sub(prefixes, "", str(uri_compcon))
    # Create the correct URL
    url = url_for('app_compcon.comparative_concept_detail', uri=uri_compcon_no_prefix)
    return f'<a href="{url}">{label_compcon}</a>'


def convert_a_tags_to_html_links(text):
    # The text in the cc yalm file uses <a> </a> to indicate hyperlinks within the cc-database
    # Use Flask's url_for to generate the actual URL
    def replace_a_tag(match):
        # Identify the label of the comparative concept that we need to link to
        label_compcon = match.group(1)
        return find_compcon_url_by_label(label_compcon)

    # Replace <a>content</a> with <a href="...">content</a>
    html_text = re.sub(
        r'<a>(.*?)</a>',
        replace_a_tag,
        text
    )
    return html_text

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

# Load the ontologies
ont = Graph()
for ttl_file in glob.glob("ontologies/*.ttl"): # for compcon
    ont.parse(ttl_file, format="turtle")

###################################################
### CREATE LIST OF COMPARATIVE CONCEPTS
###################################################

@app_compcon_blueprint.route("/")
def list_view():
    list_of_sem = list_comparative_concept_for_one_type(compcon.sem)
    list_of_inf = list_comparative_concept_for_one_type(compcon.inf)
    list_of_str = list_comparative_concept_for_one_type(compcon.str)
    list_of_cxn = list_comparative_concept_for_one_type(compcon.cxn)

    return render_template("app_compcon/list.html",
                           list_of_sem=list_of_sem,
                           list_of_inf=list_of_inf,
                           list_of_str=list_of_str,
                           list_of_cxn=list_of_cxn)


def list_comparative_concept_for_one_type(CCtype) -> list[Any]:
    list_of_CC = []

    CCtype = CCtype
    for cc in ont.subjects(predicate=RDF.type, object=CCtype):
        compcon_uri = str(cc)
        title = str(ont.value(subject=cc, predicate=RDFS.label))

        # Append construction details as dictionary
        list_of_CC.append({
            'uri': compcon_uri,
            'title': title
        })

    # Sorting in alphabetical order
    list_of_CC = sorted(
        list_of_CC,
        key=lambda x: (x['title'].lower())
    )
    return list_of_CC


###################################################
### CREATE ENTRIES FOR COMPARATIVE CONCEPTS
###################################################

@app_compcon_blueprint.route('/entry/<path:uri>', endpoint='comparative_concept_detail')
def comparative_concept_detail(uri):

    # Rebuild the full URI for the construction
    entry_uri = URIRef("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#" + uri)

    # Fetch the title to display
    type = ont.value(entry_uri, RDF.type)
    type_abbreviation = re.sub("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#","", str(type))
    title = ont.value(entry_uri, RDFS.label)
    complete_title = title + " (" + type_abbreviation + ")"

    # Collect all triples from the ontology where entry_uri is the subject
    description = []
    for predicate, obj in ont.predicate_objects(subject=entry_uri):
        if predicate == compcon.subtypeOf: # For taxonomical relations: link to the relevant comparative concept
            object_clean = get_label_or_iri(obj, g, ont)
            object_with_urls = find_compcon_url_by_label(object_clean)
        elif predicate == URIRef("http://www.w3.org/2000/01/rdf-schema#comment"): # Display the italics and hyperlinks in the definition
            predicate = "Definition"
            object_clean = get_label_or_iri(obj, g, ont)
            object_emphasized = re.sub(r'<e>(.*?)</e>', r'<em>\1</em>', object_clean)
            object_with_urls = convert_a_tags_to_html_links(object_emphasized)
        else:
            object_clean = get_label_or_iri(obj, g, ont)
            object_emphasized = re.sub(r'<e>(.*?)</e>', r'<em>\1</em>', object_clean)
            object_with_urls = convert_a_tags_to_html_links(object_emphasized)
        description.append({
            'property': get_label_or_iri(predicate, g, ont),
            'object': object_with_urls
        })
    description[:] = [item for item in description if item[
        'property'] != "http://www.w3.org/2000/01/rdf-schema#label"]  # The label is the title, therefore not needed
    description[:] = [item for item in description if item[
        'property'] != "Link to the MoCCA database of Comparative Concepts"]  # The link will be added to the sources, not needed in the main table

    # Collect constructions that use entry_uri as a comparative concept
    construction_list = []
    for subj in g.subjects(predicate=compcon.hasCompCon,object=entry_uri):
        type_of_subj = g.value(subject=subj, predicate=RDF.type)
        # two cases: either the subject of hasCompCon is a construction ...
        if type_of_subj == URIRef("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#Construction"):
            construction_uri = subj
            name = g.value(subject=construction_uri, predicate=URIRef("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasTitle"))
            url = re.sub("http://example.org/cx/","", str(construction_uri))
        # ... or the subject of hasCompCon is a construction element (then, we need to look for the construction)
        else:
            construction_uri = URIRef(re.sub(r"_\d", "", str(subj)))
            name = g.value(subject=construction_uri,
                           predicate=URIRef("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#hasTitle"))
            url = re.sub("http://example.org/cx/", "", str(construction_uri))
        construction_list.append({
            'object': name,
            'url': url,
        })

    url_in_mocca_database = ont.value(subject=entry_uri, predicate=compcon.linkToDatabase)

    return render_template("app_compcon/entry.html",
                           title = complete_title,
                           description = description,
                           constructions = construction_list,
                           url_in_mocca_database = url_in_mocca_database)