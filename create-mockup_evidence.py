from rdflib import Graph, Literal, Namespace, RDF, RDFS

# Create a Graph
g = Graph()

g.parse("instance/Submissions/FernandezSantos_20241125_105826_cx.ttl", format="turtle")

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

study = "FernandezSantos_20260130_629471"
summary = "Participants' accuracy on subject relative clauses is at ceiling only when the verb follows the relativizer. Accuracy decreases when the verb is in a clause-final position. Object relative clauses are not at ceiling, but are misinterpreted as subject relative clauses over 90% of the time when there is no object marker and the verb follows the relativizer. The presence of an object marker does not impact accuracy when the verb is clause-final."

g.add((rd[study], RDF.type, rdata.Study))
g.add((rd[study], rdata.studyType, rdata.behavioralExperiment))
g.add((rd[study], rdata.relevantFor, cx.Transitiveobjectrelativeclause))
g.add((cx.Transitiveobjectrelativeclause, rdata.basedOnStudy, rd[study]))
g.add((rd[study], rdata.dataRepository, Literal("https://osf.io/4x6pz/files/osfstorage")))
g.add((rd[study], rdata.publishedIn, Literal("Llompart, Fernández Santos & Dąbrowska (2024-10-10). Comprehension of object relatives in Spanish: the role of frequency and transparency in acquisition and adult grammar. 10.1515/cog-2024-0016"))) # TODO: real bibliography
g.add((rd[study], rdata.Summary, Literal(summary)))

# TODO create a real ontology
g.add((rdata.behavioralExperiment, RDFS.label, Literal("Behavioral experiment")))

g.serialize(destination="instance/Submissions/FernandezSantos_mockup_20250910_105826_rd.ttl", format='turtle')