from flask import Flask, request, render_template_string
from rdflib import Graph, Namespace, RDFS
from datetime import datetime
import os
import re

app = Flask(__name__)

COMP = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#")
CX = Namespace("http://example.org/cx/")

ONTOLOGY_FILE = "ontologies/compcon.ttl"
OUTPUT_DIR = "instance/Submissions"


def load_compcon_mapping():
    g = Graph()
    g.parse(ONTOLOGY_FILE)

    mapping = {}

    for s, p, o in g.triples((None, RDFS.label, None)):
        label = str(o).strip().lower()

        for cls in ["cxn", "inf", "str", "sem"]:
            if (s, None, COMP[cls]) in g:
                mapping[(label, cls)] = s

    return mapping


mapping = load_compcon_mapping()


def parse_line(line):
    """
    Extract label and class from line like:
    modification construction (cxn)
    """
    m = re.match(r"(.+?)\s*\((cxn|inf|str|sem)\)", line.strip())
    if not m:
        return None

    label = m.group(1).strip().lower()
    cls = m.group(2)

    return label, cls


def parse_input(iri, text):
    triples = []

    current_subject = CX[iri]
    ce_index = None

    for raw in text.splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("CE"):
            ce_index = line.replace("CE", "").strip()
            current_subject = CX[f"{iri}_{ce_index}"]
            continue

        if "lvl" in line:
            current_subject = CX[iri]
            continue

        parsed = parse_line(line)
        if not parsed:
            continue

        label, cls = parsed

        obj = mapping.get((label, cls))
        if obj:
            triples.append((current_subject, COMP.hasCompCon, obj))

    return triples


HTML_FORM = """
<h2>RDF Generator for Comparative Concepts</h2>
<form method="post">
IRI of the construction:<br>
<input type="text" name="iri"><br><br>

Copy-paste your manual annotation:<br>
<textarea name="content" rows="20" cols="60"></textarea><br><br>

<input type="submit">
</form>
"""


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        iri = request.form["iri"].strip()
        text = request.form["content"]

        triples = parse_input(iri, text)

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Petrenko_compcon_{timestamp}_cx.ttl"
        path = os.path.join(OUTPUT_DIR, filename)

        g = Graph()

        g.bind("compcon", COMP)
        g.bind("cx", CX)

        for s, p, o in triples:
            g.add((s, p, o))

        g.serialize(destination=path, format="turtle")

        return f"File written: {path}"

    return render_template_string(HTML_FORM)


if __name__ == "__main__":
    app.run(debug=True)