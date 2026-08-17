from flask import Blueprint, render_template
from rdflib import Graph, URIRef
from datetime import date
from graph_loader import (g, cx, rd, membr)

# Create the blueprint for the main app
main_blueprint = Blueprint('main', __name__, template_folder='../templates')

# Define the route for the landing page
@main_blueprint.route("/")
def home():
    return render_template("index.html")

@main_blueprint.route("/impressum")
def impressum():
    return render_template("impressum.html")

@main_blueprint.route("/cc-project")
def cc_project():
    return render_template("cc-project.html")

@main_blueprint.route("/stats")
def stats():

    # Count classes and properties in the ontology:
    ontology_files = [
        "ontologies/casa.rdf",
        "ontologies/compcon.ttl",
        "ontologies/evid.rdf",
        "ontologies/gest.rdf",
        "ontologies/lg.rdf",
        "ontologies/links-1.1.rdf",
        "ontologies/rcxn.rdf",
        "ontologies/rsrch.rdf"
    ]
    ont = Graph()
    for file_path in ontology_files:
        if file_path.endswith(".owl") or file_path.endswith(".rdf"):
            ont.parse(file_path, format="xml")
        elif file_path.endswith(".ttl"):
            ont.parse(file_path, format="turtle")

    # --- Count Classes ---
    classes_query = """
            SELECT (COUNT(DISTINCT ?class) AS ?count)
            WHERE {
                ?class a owl:Class .
            }
        """
    class_result = ont.query(classes_query)
    num_classes = class_result.bindings[0]['count'].value

    # --- Count Properties ---
    properties_query = """
            SELECT (COUNT(DISTINCT ?prop) AS ?count)
            WHERE {
                ?prop a owl:ObjectProperty .
            }
        """
    prop_result = ont.query(properties_query)
    num_properties = prop_result.bindings[0]['count'].value

    # Count triplets for cx.ttl
    counter_cx = 0
    for s, p, o in g:
        if isinstance(s, URIRef) and str(s).startswith(cx):
            counter_cx = counter_cx + 1

    # NB: For the moment, we save research data into cx. TODO: should we put them in their own Abox?
    for s, p, o in g:
        if isinstance(s, URIRef) and str(s).startswith(rd):
            counter_cx = counter_cx + 1

    # Count triplets for membr.ttl
    counter_membr = 0
    for s, p, o in g:
        # Check if the subject starts with the desired prefix
        if isinstance(s, URIRef) and str(s).startswith(membr):
            counter_membr = counter_membr + 1

    # Count triplets in reference.ttl
    counter_references = 0
    for subject, reference in g.subject_objects(cx.hasLiterature):
        for p, o in g.predicate_objects(reference):
            counter_references = counter_references + 1

    # Count total of triplets
    counter = counter_cx + counter_membr + counter_references

    # Count the non-gesture constructions
    query_nongesture = """
        PREFIX rcxn: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#>
        SELECT DISTINCT ?construction
        WHERE {
            ?construction a rcxn:Construction .
        }
        """
    results_nongesture = g.query(query_nongesture)
    num_nongesture = len(results_nongesture)

    query_gesture = """
            PREFIX rcxn: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#>
            SELECT DISTINCT ?construction
            WHERE {
                ?construction a gest:GestureConstruction .
            }
            """
    results_gesture = g.query(query_gesture)
    num_gesture = len(results_gesture)

    num_constructions = num_nongesture + num_gesture

    # Count the contributors
    query_contributors = """
            PREFIX rcxn: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#>
            SELECT DISTINCT ?contributor
            WHERE {
                ?construction a rcxn:Construction .
                ?construction rcxn:hasMetadata ?metadata .
                ?metadata rcxn:annotator ?contributor .
            }
            """
    results_contributors = g.query(query_contributors)
    num_contributors = len(results_contributors)

    # Date of call
    last_updated = date.today().strftime("%dth of %B %Y")

    return render_template("stats.html",
                           num_classes=num_classes,
                           num_properties=num_properties,
                           counter_cx=counter_cx,
                           counter_membr=counter_membr,
                           counter_references=counter_references,
                           counter=counter,
                           num_constructions=num_constructions,
                           num_nongesture=num_nongesture,
                           num_gesture=num_gesture,
                           num_contributors=num_contributors,
                           last_updated=last_updated)