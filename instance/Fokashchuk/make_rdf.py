import pandas as pd
from datetime import datetime
from rdflib import Graph, Namespace, URIRef, Literal, RDF, DCTERMS, XSD

# Load the graphs and namespaces defined in graph_loader.py
from graph_loader import (g, ont, casa, cx, compcon, evid, frac, gest, lg, links, membr, olia, oliatop, rcxn, rsrch)


# Read Excel file
df = pd.read_excel("data.xlsx")

# Create RDF graph
g = Graph()

# Bind namespace
g.bind("cx", cx)
g.bind("lg", lg)
g.bind("links", links)
g.bind("membr", membr)
g.bind("rcxn", rcxn)
g.bind("rsrch", rsrch)

# Functions
def clean_name(name):
    original = str(name)
    clean = original.replace(" ", "")
    clean = clean.replace("?", "")
    clean = clean.replace("!", "")
    clean = clean.replace(".", "")
    clean = clean.replace(":", "")
    clean = clean.replace(",", "")
    clean = clean.replace("-", "")
    clean = clean.replace("[", "")
    clean = clean.replace("]", "")
    clean = clean.replace("(", "")
    clean = clean.replace(")", "")
    clean = clean.replace("/", "")
    clean = clean.replace("'","")
    clean = clean.replace("ß", "ss")
    clean = clean.replace("á", "a")
    clean = clean.replace("â", "a")
    clean = clean.replace("é", "e")
    clean = clean.replace("ë", "e")
    clean = clean.replace("î", "i")
    clean = clean.replace("ä", "ae")
    clean = clean.replace("ö", "oe")
    clean = clean.replace("ü", "ue")
    clean = clean.replace("Ä","AE")
    clean = clean.replace("Ö", "OE")
    clean = clean.replace("Ü", "UE")
    clean = clean.replace("ā", "aa")
    clean = clean.replace("+", "PLUS")
    clean = clean.replace("&", "AND")
    clean = clean.replace("/", "SLASH")
    return clean

# Convert rows into triples
for _, row in df.iterrows():

    #constant
    construction_language_uri = "deu"

    # General and metadata
    construction_name = row['DE: Construction']
    construction_name_cleaned = construction_language_uri + "_" + clean_name(construction_name)
    meaning = f"{row['DE: Meaning (DWDS)']} (DWDS)"
    g.add((cx[construction_name_cleaned], RDF.type, rcxn.Construction))
    metadata_uri = f"{construction_name_cleaned}_MD"
    g.add((cx[metadata_uri], RDF.type, rcxn.Metadata))
    g.add((cx[construction_name_cleaned], rcxn.hasMetadata, cx[metadata_uri]))
    g.add((cx[metadata_uri], rcxn.annotator, membr.Fokashchuk))
    g.add((cx[metadata_uri], DCTERMS.created, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
    g.add((membr.Project_Fokashchuk_241210_F250218, rsrch.basedOn, cx[construction_name_cleaned]))
    construction_complete_title = f"{construction_name}"
    g.add((cx[construction_name_cleaned], rcxn.hasTitle, Literal(construction_complete_title)))
    g.add((cx[construction_name_cleaned], lg.partOfLanguage, lg[construction_language_uri]))

    # Meaning of the construction
    cx_meaning_uri = f"{construction_name_cleaned}_Meaning"
    g.add((cx[cx_meaning_uri], RDF.type, rcxn.ConstructionMeaning))
    g.add((cx[construction_name_cleaned], rcxn.hasConstructionMeaning, cx[cx_meaning_uri]))
    g.add((cx[cx_meaning_uri], rcxn.hasMeaning, Literal(meaning)))

    # sequence of construction elements
    seq_slots = URIRef(cx[f"{construction_name_cleaned}_slots"])
    g.add((seq_slots, RDF.type, RDF.Seq))
    g.add((cx[construction_name_cleaned], rcxn.hasSlots, seq_slots))
    NP1_element_uri = cx[f"{construction_name_cleaned}_{1}"]
    PP_element_uri = cx[f"{construction_name_cleaned}_{2}"]
    NP2_element_uri = cx[f"{construction_name_cleaned}_{3}"]
    g.add((seq_slots, URIRef(RDF["_1"]), NP1_element_uri))
    g.add((seq_slots, URIRef(RDF["_2"]), PP_element_uri))
    g.add((seq_slots, URIRef(RDF["_3"]), NP2_element_uri))

    # Semantics of construction elements
    NP1_sem = row['DE: Semantics of NP1']
    PP_sem = row['DE: Semantics of PP']
    NP2_sem = row['DE: Semantics of NP2']
    g.add((NP1_element_uri, rcxn.hasOtherSemanticContribution, Literal(NP1_sem)))
    g.add((PP_element_uri, rcxn.hasOtherSemanticContribution, Literal(PP_sem)))
    g.add((NP2_element_uri, rcxn.hasOtherSemanticContribution, Literal(NP2_sem)))

    # Syntactic form of element 1
    NP1_form_uri = cx[f"{construction_name_cleaned}_{1}_Form"]
    g.add((NP1_element_uri, rcxn.hasSlotForm, NP1_form_uri))
    g.add((NP1_form_uri, RDF.type, rcxn.SlotForm))
    NP1_head = row['DE: Head of NP1']
    if NP1_head == "X" :
        # TODO: make sure german noun cx exist
        g.add((NP1_form_uri, rcxn.hasSyntacticForm, cx.deu_Noun))
    else:
        cleaned_stem_construction = "deu_" + clean_name(NP1_head)
        metadata_stem_construction = f"{cleaned_stem_construction}_MD"
        g.add((cx[cleaned_stem_construction], RDF.type, rcxn.Construction))
        g.add((cx[cleaned_stem_construction], lg.partOfLanguage, lg.deu))
        g.add((cx[cleaned_stem_construction], rcxn.hasMetadata, cx[metadata_stem_construction]))
        g.add((cx[metadata_stem_construction], RDF.type, rcxn.Metadata))
        g.add((cx[metadata_stem_construction], rcxn.annotator, membr.Fokashchuk))
        g.add((cx[metadata_stem_construction], DCTERMS.created,
               Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
        g.add((cx[cleaned_stem_construction], rcxn.hasTitle, Literal(NP1_head)))
        g.add((NP1_form_uri, rcxn.hasStem, cx[cleaned_stem_construction]))
        g.add((cx[cleaned_stem_construction], links.elementOf, cx[construction_name_cleaned]))

    # Syntactic form of element 2
    PP_form_uri = cx[f"{construction_name_cleaned}_{2}_Form"]
    g.add((PP_element_uri, rcxn.hasSlotForm, PP_form_uri))
    g.add((PP_form_uri, RDF.type, rcxn.SlotForm))
    PP_prep_uri = f"deu_{row['DE: Preposition']}"
    # TODO make sure an and auf exist as cx
    g.add((PP_form_uri, rcxn.hasStem, cx[PP_prep_uri]))

    # Syntactic form of element 3
    NP2_form_uri = cx[f"{construction_name_cleaned}_{3}_Form"]
    g.add((NP2_element_uri, rcxn.hasSlotForm, NP2_form_uri))
    g.add((NP2_form_uri, RDF.type, rcxn.SlotForm))
    NP1_head = row['DE: Head of NP2']



# 5. Save as Turtle
g.serialize(destination="Fokashchuk_cx.ttl", format="turtle")