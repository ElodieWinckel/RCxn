from rdflib import Graph
import glob

# Create a new RDF graph
g = Graph()

# Load your RDF data (assuming you have a Turtle file)
for ttl_file in glob.glob("user_graphs/*_cx.ttl"):
    g.parse(ttl_file, format="turtle")

# Define the SPARQL query
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

# Execute the query
results = g.query(query)

# Print the results
for row in results:
    print(f"Construction: {row.construction}, Title: {row.title}")
