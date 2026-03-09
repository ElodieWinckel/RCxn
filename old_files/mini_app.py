from flask import Flask, request, render_template, send_file
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mini_html.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Fields in category "General"
    construction_name = request.form['construction']
    construction_name_cleaned = construction_name.replace(" ", "")
    construction_language = request.form['language']
    # Fields in category "Form-meaning pairings of the elements"
    element_nb = int(request.form['element_nb'])

    # The name of the construction is a concatenation of the language and the title
    construction_complete_title = f"{construction_language} {construction_name}"

    # Create RDF graph
    g = Graph()
    cx = Namespace("http://example.org/cx/")
    membr = Namespace("http://example.org/users/")
    olia = Namespace("http://purl.org/olia/olia.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    g.bind("cx", cx)
    g.bind("membr", membr)

    # Create RDF triples
    g.add((cx[construction_name_cleaned], RDF.type, membr.Construction))
    # Add creation date as today.
    g.add((cx[construction_name_cleaned], cx.createdOn, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
    g.add((cx[construction_name_cleaned], cx.hasTitle, Literal(construction_complete_title)))

    #Create the sequence of construction elements
    ## Create a new blank node for the sequence
    seq_slots = URIRef(cx[f"{construction_name_cleaned}_slots"])
    g.add((seq_slots, RDF.type, RDF.Seq))
    # Add elements to the sequence
    for i in range(element_nb):
        element_uri = cx[f"{construction_name_cleaned}_{chr(65 + i)}"]
        seq_position = URIRef(RDF[f"_{i + 1}"])
        g.add((seq_slots, seq_position, element_uri))
    ## Add the sequence as the object of the triple
    g.add((cx[construction_name_cleaned], cx.hasSlots, seq_slots))

    # Process multiple checkboxes for topic, comment, focus, and background
    topics = request.form.getlist('topic_element[]')
    comments = request.form.getlist('comment_element[]')
    focuses = request.form.getlist('focus_element[]')
    backgrounds = request.form.getlist('background_element[]')
    # Validate incompatible selections (same element as both topic and comment, or focus and background)
    if set(topics) & set(comments):
        return "Error: An element cannot be both Topic and Comment."
    if set(focuses) & set(backgrounds):
        return "Error: An element cannot be both Focus and Background."

    # Add triples for topic, comment, focus, and background
    for topic in topics:
        g.add((cx[topic], cx.hasIS, cx.Topic))
    for comment in comments:
        g.add((cx[comment], cx.hasIS, cx.Comment))
    for focus in focuses:
        g.add((cx[focus], cx.hasIS, cx.Focus))
    for background in backgrounds:
        g.add((cx[background], cx.hasIS, cx.Background))



    #A loop that adds the value of the fields related to the slots for each slot.
    for i in range(1, element_nb + 1):
        y = i -1
        element_uri = URIRef(cx[f"{construction_name_cleaned}_{chr(65 + y)}"])
        word_order = request.form[f'WordOrder_{i}']
        if word_order.strip():
            g.add((element_uri, cx.WordOrder, Literal(word_order)))#

    # Handle the dynamically added examples
    example_counter = 1
    while f'example_text_{example_counter}' in request.form:
            # Fetch values for each example
            example_text = request.form[f'example_text_{example_counter}']
            translation = request.form[f'translation_{example_counter}']
            glosses = request.form[f'glosses_{example_counter}']
            comment = request.form[f'comment_{example_counter}']

            # Create a unique URI for each example
            example_uri = cx[f"{construction_name_cleaned}_Ex_{chr(64 + example_counter)}"]

            # Add RDF triples for the example
            g.add((cx[construction_name_cleaned], cx.hasExample, example_uri))
            g.add((example_uri, RDF.type, cx.Example))
            g.add((example_uri, cx.hasTranslation, Literal(translation)))
            g.add((example_uri, cx.hasGlosses, Literal(glosses)))
            g.add((example_uri, RDFS.comment, Literal(comment)))

            example_counter += 1

    # Serialize the updated RDF graph to a .ttl file
    file_path = f'{construction_language.split("/")[-1]}_cx.ttl'
    g.serialize(destination=file_path, format='turtle')

    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
