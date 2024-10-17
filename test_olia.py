from flask import Flask, request, render_template, send_file
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from datetime import datetime
import os

def load_SemanticRoles(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl")
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    role_names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.SemanticRole)]
    return role_names

semantic_roles = load_SemanticRoles('olia.owl')
print(semantic_roles)

def load_NumberFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl")
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.NumberFeature)]
    return names

number_features = load_NumberFeatures('olia.owl')
print(number_features)


def load_CaseFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl")
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.CaseFeature)]
    names = [(str(s).replace("Case", "")) for s in names]
    return names

case_features = load_CaseFeatures('olia.owl')
print(case_features)


def load_TenseFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')

    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

    tense_features = []

    # Find all subclasses and get their labels
    for subclass in g.subjects(RDFS.subClassOf, oliatop.TenseFeature):
        label = g.value(subclass, RDFS.label, None)
        if label:
            tense_features.append((str(subclass), str(label)))

        # Find subclasses of subclasses
        for indirect_subclass in g.subjects(RDFS.subClassOf, subclass):
            label = g.value(indirect_subclass, RDFS.label, None)
            if label:
                tense_features.append((str(indirect_subclass), str(label)))

    # Sort by label
    tense_features = sorted(tense_features, key=lambda x: x[1].lower())

    return tense_features

tense_features = load_TenseFeatures('olia.owl')
print(tense_features)

def load_Mode(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, olia.FiniteVerb)]
    names = [(str(s).replace("Verb", "")) for s in names]
    return names

modus = load_Mode('olia.owl')
print(modus)

def load_VoiceFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl")
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.VoiceFeature)]
    names = [(str(s).replace("Voice", "")) for s in names]
    return names

voice_features = load_VoiceFeatures('olia.owl')
print(voice_features)

# Load URIs of already existing constructions (cx.ttl)
def load_existing_constructions_uri(file_path):
    g = Graph()
    g.parse(file_path, format='ttl')
    membr = Namespace("http://example.org/users/")
    names = [(str(s).replace("http://example.org/cx/", "")) for s in g.subjects(RDF.type, membr.Construction)]
    return names
list_of_cxs_URI = load_existing_constructions_uri("cx.ttl")
print(list_of_cxs_URI)

# Load URIs and title of already existing constructions (cx.ttl)
def load_existing_constructions_title(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    membr = Namespace("http://example.org/users/")
    cx = Namespace("http://example.org/cx/")
    names = [str(g.value(s, cx.hasTitle)) for s in g.subjects(RDF.type, membr.Construction)]
    return names

cxs = load_existing_constructions_title("cx.ttl")
print(cxs)