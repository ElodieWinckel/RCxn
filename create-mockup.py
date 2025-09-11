from argparse import Namespace

from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS

# Create a Graph
g = Graph()

g.parse("instance/Submissions/FernandezSantos_mockup_20250910_105826_rd.ttl", format="turtle")

# Define the namespaces
cx = Namespace("http://example.org/cx/")
g.bind("cx", cx)
olia = Namespace("http://purl.org/olia/olia.owl#")
g.bind("olia", olia)
rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
g.bind("rcxn", rcxn)
rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
g.bind("rsrch", rsrch)
lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
g.bind("lg", lg)
rd = Namespace("http://example.org/rd/")
g.bind("rd", rd)
rdata = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rdata#")
g.bind("rdata", rdata)

study = "FernandezSantos_20250910_629471"
picture1 = study + "_picture1"
summary = "Participants' accuracy on subject relative clauses is at ceiling only when the verb follows the relativizer. Accuracy decreases when the verb is in a clause-final position. Object relative clauses are not at ceiling, but are misinterpreted as subject relative clauses over 90% of the time when there is no object marker and the verb follows the relativizer. The presence of an object marker does not impact accuracy when the verb is clause-final."

g.add((rd[study], RDF.type, rdata.Study))
g.add((rd[study], rdata.studyType, rdata.behavioral))
g.add((rd[study], rdata.hasTitle, Literal("Predictive processing can override perceptual information: evidence from Spanish object relative clauses [Study 1]")))
g.add((rd[study], rdata.relevantFor, cx.Transitiveobjectrelativeclause))
g.add((cx.Transitiveobjectrelativeclause, rdata.basedOnStudy, rd[study]))
g.add((rd[study], rdata.Visualization, rd[picture1]))
g.add((rd[picture1], rdata.belongsTo, rd[study]))
g.add((rd[study], rdata.dataRepository, Literal("https://osf.io/4x6pz/files/osfstorage")))
g.add((rd[study], rdata.publishedIn, rd.FernandezSantos_20250910_629471_Sources))
g.add((rd[study], rdata.Summary, Literal(summary)))

g.serialize(destination="instance/Submissions/FernandezSantos_mockup_20250910_105826_rd.ttl", format='turtle')