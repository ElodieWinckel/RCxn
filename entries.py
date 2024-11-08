import glob
from flask import Flask, render_template, redirect, url_for
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD

app = Flask(__name__)

# Load and parse all RDF files ending in "_cx.ttl" from a specific folder
g = Graph()

for ttl_file in glob.glob("user_graphs/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Define the namespaces
CX = Namespace("http://example.org/cx/")
g.bind("cx", CX)
membr = Namespace("http://example.org/users/")
g.bind("membr", membr)
olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
g.bind("RDFS", RDFS)


@app.route('/')
def index():
    constructions = []

    # SPARQL query to get the title for each construction via the metadata URI
    query = """
    PREFIX cx: <http://example.org/cx/>
    PREFIX membr: <http://example.org/users/>
    SELECT ?construction ?title
    WHERE {
        ?construction a membr:Construction .
        ?construction cx:hasMetadata ?meta .
        ?meta cx:hasTitle ?title .
    }
    """

    # Execute the SPARQL query
    results = g.query(query)

    # Process query results
    for row in results:
        construction_uri = str(row.construction)
        title = str(row.title)

        # Append construction details as dictionary
        constructions.append({
            'uri': construction_uri,
            'title': title
        })

    return render_template('index_entries.html', constructions=constructions)


@app.route('/construction/<path:uri>', endpoint='construction_detail')
def construction_detail(uri):
    # Rebuild the full URI for the construction
    entry_uri = URIRef("http://example.org/cx/" + uri)

    # Collect all triples where entry_uri is the subject
    triples = []
    for predicate, obj in g.predicate_objects(subject=entry_uri):
        triples.append({
            'property': str(predicate),
            'object': str(obj)
        })

    # Fetch the title for display purposes
    entry_metadata_uri = URIRef(str(entry_uri) + "_MD")
    title = g.value(entry_metadata_uri, CX.hasTitle)

    return render_template("construction.html", title=title, triples=triples)


if __name__ == "__main__":
    app.run(debug=True)
