from rdflib import Graph, Literal, Namespace, RDF, RDFS

# Create a Graph
g = Graph()

#g.parse("instance/Submissions/Iabdounane_thiscloseto_20260202_102248_cx.ttl", format="turtle")

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

g.add((cx.eng_ThisclosetoVingconstruction, cx.usesGesture, cx.SmallQuantityGestureConstruction)) # TODO usesGesture in gstr
g.add((cx.SmallQuantityGestureConstruction, RDF.type, cx.GestureConstruction)) # TODO GestureConstruction in rcxn
g.add((cx.SmallQuantityGestureConstruction, lg.partOfLanguage, lg.eng))

g.add((cx.SmallQuantityGestureConstruction, cx.stratsOnSlot, cx.eng_ThisclosetoVingconstruction_1)) # TODO stratsOnSlot gstr
g.add((cx.SmallQuantityGestureConstruction, cx.endsOnSlot, cx.eng_ThisclosetoVingconstruction_6)) # TODO endsOnSlot in gstr
g.add((cx.SmallQuantityGestureConstruction, cx.hasPhases, Literal("1"))) # TODO hasPhases in gstr
g.add((cx.SmallQuantityGestureConstruction, rcxn.hasTitle, Literal("Small Quantity Gesture Construction")))
g.add((cx.SmallQuantityGestureConstruction, cx.hasForm, cx.SmallQuantityGestureConstruction_Form)) # TODO hasForm in rcxn
g.add((cx.SmallQuantityGestureConstruction, rcxn.hasMeaning, cx.SmallQuantityGestureConstruction_Meaning))

# Form # TODO all properties in gstr
g.add((cx.SmallQuantityGestureConstruction_Form, cx.handshape, Literal("Thumb and index extended or crooked and parallel to each other.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.handshape, Literal("Middle, right, and little fingers retracted toward the palm.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.orientation, Literal("Palm Lateral.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.movement, Literal("Static hold or beat.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.position, Literal("Central space or at face level.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.handedness, Literal("One-handed.")))
g.add((cx.SmallQuantityGestureConstruction_Form, cx.duration, Literal("Usually for the entire duration of the co-occurring verbal construction.")))

# Meaning # TODO all properties in gstr
g.add((cx.SmallQuantityGestureConstruction_Meaning, cx.semanticProperty, Literal("Small quantity.")))
g.add((cx.SmallQuantityGestureConstruction_Meaning, cx.pragmaticProperty, Literal("Affective/evaluative framing.")))
g.add((cx.SmallQuantityGestureConstruction_Meaning, cx.pragmaticProperty, Literal("Foregrounding the small quantity of the referent.")))

g.serialize(destination="instance/Submissions/Iabdounane_mockup_thiscloseto_20260202_102248_gesture.ttl", format='turtle')