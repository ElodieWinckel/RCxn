import glob
import os

from rdflib import (
    Graph,
    Namespace,
)

###################################################
### CREATE RDF GRAPH FOR DATABASE
###################################################

g = Graph()

# Check if the production directory exists (otherwise, defaults to development directory)
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path

else:
    # Load and parse all RDF files from the folder with submissions (only during development process)
    for ttl_file in glob.glob("instance/Submissions/**/*.ttl", recursive=True):
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
dcterm = Namespace("http://purl.org/dc/terms/")
g.bind("dcterm",dcterm)
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
compcon = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#")
g.bind("compcon", compcon)

###################################################
### CREATE RDF GRAPH FOR ONTOLOGIES
###################################################

ont = Graph()
for xlm_file in glob.glob("ontologies/*.rdf"):
    ont.parse(xlm_file, format="xml")
for xlm_file in glob.glob("ontologies/*.owl"): # for olia
    ont.parse(xlm_file, format="xml")
for ttl_file in glob.glob("ontologies/*.ttl"): # for compcon
    ont.parse(ttl_file, format="turtle")

