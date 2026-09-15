import pandas as pd
from datetime import datetime
from rdflib import Graph, Namespace, URIRef, Literal, RDF, DCTERMS, XSD, RDFS

# Load the graphs and namespaces defined in graph_loader.py
from graph_loader import (g, ont, casa, cx, compcon, evid, frac, gest, lg, links, membr, olia, oliatop, rcxn, rsrch)


# Read Excel file
df = pd.read_excel("data_modified.xlsx")

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

################################################################
### GERMAN CONSTRUCTION
################################################################

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

    # Sequence of construction elements
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
    PP_prep = row['DE: Preposition']
    # TODO make sure an and auf exist as cx
    g.add((PP_form_uri, rcxn.hasSurfaceForm, Literal(PP_prep)))

    # Syntactic form of element 3
    NP2_form_uri = cx[f"{construction_name_cleaned}_{3}_Form"]
    g.add((NP2_element_uri, rcxn.hasSlotForm, NP2_form_uri))
    g.add((NP2_form_uri, RDF.type, rcxn.SlotForm))
    g.add((NP2_form_uri, rcxn.hasSyntacticForm, cx.deu_NounPhrase))
    if row['DE: Head of NP2'] != "Y":
        NP2_head = f'head is "{row['DE: Head of NP2']}"'
        g.add((NP2_form_uri, RDFS.comment, Literal(NP2_head)))
    if row['DE: Case of NP2'] == "ACC.":
        NP2_case = "Accusative"
        g.add((NP2_element_uri, olia.hasCase, olia[NP2_case]))
    if row['DE: Case of NP2'] == "DAT.":
        NP2_case = "DativeCase"
        g.add((NP2_element_uri, olia.hasCase, olia[NP2_case]))

    # Example
    if not pd.isna(row['DE: Construct (example from SKELL)']):
        example = row['DE: Construct (example from SKELL)']
        words = example.split()
        first = f"[{words[0]}]1"
        second = f" [{words[1]}]2"
        remaining = ' '.join(words[2:])
        third = f" [{remaining}]3"
        annotated_example = first + second + third
        example_uri = cx[f"{construction_name_cleaned}_Ex_A"]
        g.add((cx[construction_name_cleaned], cx.hasExample, example_uri))
        g.add((example_uri, RDF.type, cx.Example))
        g.add((example_uri, cx.hasAnnotatedText, Literal(annotated_example)))
        g.add((example_uri, cx.hasText, Literal(example)))

################################################################
### ENGLISH CONSTRUCTION
################################################################

    # General and link
    if pd.notna(row['Equivalent English']) and row['Equivalent English'] != "":
        eng_construction_language_uri = "engLME"
        eng_construction_name = row['Equivalent English']
        eng_construction_name_cleaned = eng_construction_language_uri + "_" + clean_name(eng_construction_name)
        g.add((cx[eng_construction_name_cleaned], RDF.type, rcxn.Construction))
        eng_metadata_uri = f"{eng_construction_name_cleaned}_MD"
        g.add((cx[eng_metadata_uri], RDF.type, rcxn.Metadata))
        g.add((cx[eng_construction_name_cleaned], rcxn.hasMetadata, cx[eng_metadata_uri]))
        g.add((cx[eng_metadata_uri], rcxn.annotator, membr.Fokashchuk))
        g.add((cx[eng_metadata_uri], DCTERMS.created, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
        g.add((membr.Project_Fokashchuk_241210_F250218, rsrch.basedOn, cx[eng_construction_name_cleaned]))
        eng_construction_complete_title = f"{eng_construction_name}"
        g.add((cx[eng_construction_name_cleaned], rcxn.hasTitle, Literal(eng_construction_complete_title)))
        g.add((cx[eng_construction_name_cleaned], lg.partOfLanguage, lg[eng_construction_language_uri]))
        g.add((cx[eng_construction_name_cleaned], links.CL_similarFormSameFunction, cx[construction_name_cleaned]))

        # Meaning of the English construction
        eng_cx_meaning_uri = f"{eng_construction_name_cleaned}_Meaning"
        g.add((cx[eng_cx_meaning_uri], RDF.type, rcxn.ConstructionMeaning))
        g.add((cx[eng_construction_name_cleaned], rcxn.hasConstructionMeaning, cx[eng_cx_meaning_uri]))
        g.add((cx[eng_cx_meaning_uri], rcxn.hasMeaning, Literal(meaning))) # same meaning as german!

        # sequence of construction elements for English construction
        eng_seq_slots = URIRef(cx[f"{eng_construction_name_cleaned}_slots"])
        g.add((eng_seq_slots, RDF.type, RDF.Seq))
        g.add((cx[eng_construction_name_cleaned], rcxn.hasSlots, eng_seq_slots))
        eng_NP1_element_uri = cx[f"{eng_construction_name_cleaned}_{1}"]
        eng_PP_element_uri = cx[f"{eng_construction_name_cleaned}_{2}"]
        eng_NP2_element_uri = cx[f"{eng_construction_name_cleaned}_{3}"]
        g.add((eng_seq_slots, URIRef(RDF["_1"]), eng_NP1_element_uri))
        g.add((eng_seq_slots, URIRef(RDF["_2"]), eng_PP_element_uri))
        g.add((eng_seq_slots, URIRef(RDF["_3"]), eng_NP2_element_uri))

        # Syntactic form of element 1
        eng_NP1_form_uri = cx[f"{eng_construction_name_cleaned}_{1}_Form"]
        g.add((eng_NP1_element_uri, rcxn.hasSlotForm, eng_NP1_form_uri))
        g.add((eng_NP1_form_uri, RDF.type, rcxn.SlotForm))
        eng_NP1_head = row['ENG: Head of NP1']
        eng_cleaned_stem_construction = "eng_" + clean_name(eng_NP1_head)
        eng_metadata_stem_construction = f"{eng_cleaned_stem_construction}_MD"
        g.add((cx[eng_cleaned_stem_construction], RDF.type, rcxn.Construction))
        g.add((cx[eng_cleaned_stem_construction], lg.partOfLanguage, lg.eng))
        g.add((cx[eng_cleaned_stem_construction], rcxn.hasMetadata, cx[eng_metadata_stem_construction]))
        g.add((cx[eng_metadata_stem_construction], RDF.type, rcxn.Metadata))
        g.add((cx[eng_metadata_stem_construction], rcxn.annotator, membr.Fokashchuk))
        g.add((cx[eng_metadata_stem_construction], DCTERMS.created,
               Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
        g.add((cx[eng_cleaned_stem_construction], rcxn.hasTitle, Literal(eng_NP1_head)))
        g.add((eng_NP1_form_uri, rcxn.hasStem, cx[eng_cleaned_stem_construction]))
        g.add((cx[eng_cleaned_stem_construction], links.elementOf, cx[eng_construction_name_cleaned]))

        # Syntactic form of element 2
        eng_PP_form_uri = cx[f"{eng_construction_name_cleaned}_{2}_Form"]
        g.add((eng_PP_element_uri, rcxn.hasSlotForm, eng_PP_form_uri))
        g.add((eng_PP_form_uri, RDF.type, rcxn.SlotForm))
        if '/' in row['ENG: Preposition']:
            parts = [part.strip() for part in row['ENG: Preposition'].split('/', 1)]
            eng_PP_prep_1 = parts[0] if len(parts) > 0 else ""
            eng_PP_prep_2 = parts[1] if len(parts) > 1 else ""
            g.add((eng_PP_form_uri, rcxn.hasSurfaceForm, Literal(eng_PP_prep_1)))
            g.add((eng_PP_form_uri, rcxn.hasSurfaceForm, Literal(eng_PP_prep_2)))
        else:
            eng_PP_prep = row['ENG: Preposition']
            g.add((eng_PP_form_uri, rcxn.hasSurfaceForm, Literal(eng_PP_prep)))

        # Syntactic form of element 3
        eng_NP2_form_uri = cx[f"{eng_construction_name_cleaned}_{3}_Form"]
        g.add((eng_NP2_element_uri, rcxn.hasSlotForm, eng_NP2_form_uri))
        g.add((eng_NP2_form_uri, RDF.type, rcxn.SlotForm))
        g.add((eng_NP2_form_uri, rcxn.hasSyntacticForm, cx.eng_NounPhrase))
        if row['ENG: Head of NP2'] != "Y":
            eng_NP2_head = f'head is "{row['ENG: Head of NP2']}"'
            g.add((eng_NP2_form_uri, RDFS.comment, Literal(eng_NP2_head)))

# 5. Save as Turtle
g.serialize(destination="Fokashchuk_cx.ttl", format="turtle")