from flask import Flask, request, render_template, send_file
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from datetime import datetime
import json

app = Flask(__name__)

###################################################
### FUNCTIONS REQUIRED TO EXTRACT FROM DATABASES AND ONTOLOGIES
###################################################

# Load URIs and family names from existing database of researchers (users.ttl)
def load_uris_from_ttl(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    foaf = Namespace('http://xmlns.com/foaf/0.1/')
    uris_and_names = [(str(s).replace("http://example.com/users/", ""),
                       str(g.value(s, foaf.familyName))) for s in g.subjects(RDF.type, foaf.Person)]
    return uris_and_names

# Load URIs and project names from existing database of research projects (users.ttl)
def load_projects_from_ttl(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    membr = Namespace("http://example.com/users/")
    uris_and_names = [(str(s).replace("http://example.com/users/", ""),
                       str(g.value(s, membr.projectName))) for s in g.subjects(RDF.type, membr.Project)]
    return uris_and_names

# Loads URIs of semantic roles in OLIA
def load_SemanticRoles(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    role_names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.SemanticRole)]
    role_names = [(str(s).replace("Role", "")) for s in role_names]
    role_names.sort()
    return role_names

# Loads URIs of number features in OLIA
def load_NumberFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.NumberFeature)]
    names.sort()
    return names

# Loads URIs of case features in OLIA + delete "Case" at the end of URI
def load_CaseFeatures(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, oliatop.CaseFeature)]
    names = [(str(s).replace("Case", "")) for s in names]
    names.sort()
    return names

# Loads URIs of tense features in OLIA (classes and subclasses thereof)
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

# Loads URIs of modes in OLIA + delete "Verb" at the end of URI
def load_Mode(file_path):
    g = Graph()
    g.parse(file_path, format='xml')
    olia = Namespace("http://purl.org/olia/olia.owl#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    names = [(str(s).replace("http://purl.org/olia/olia.owl#", "")) for s in g.subjects(RDFS.subClassOf, olia.FiniteVerb)]
    names = [(str(s).replace("Verb", "")) for s in names]
    names.sort()
    return names

# Load URIs of already existing constructions (cx.ttl)
def load_existing_constructions_uri(file_path):
    g = Graph()
    g.parse(file_path, format='ttl')
    membr = Namespace("http://example.org/users/")
    names = [(str(s).replace("http://example.org/cx/", "")) for s in g.subjects(RDF.type, membr.Construction)]
    return names

# Load URIs and title of already existing constructions (cx.ttl)
def load_existing_constructions_title(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    membr = Namespace("http://example.org/users/")
    cx = Namespace("http://example.org/cx/")
    names = [str(g.value(s, cx.hasTitle)) for s in g.subjects(RDF.type, membr.Construction)]
    return names

###################################################
### RUN HTML FORM
###################################################

# Prepare all lists that are passed to the HTML form
uri_list = load_uris_from_ttl('../Abox/users.ttl')
project_list = load_projects_from_ttl('../Abox/users.ttl')
semantic_roles = load_SemanticRoles('../ontologies/olia.owl')
semantic_roles.insert(0, '') # The first element of the drop-down list should be the empty string
number_features = load_NumberFeatures('../ontologies/olia.owl')
number_features.insert(0, '') # The first element of the drop-down list should be the empty string
case_features = load_CaseFeatures('../ontologies/olia.owl')
case_features.insert(0, '') # The first element of the drop-down list should be the empty string
tense_features = load_TenseFeatures('../ontologies/olia.owl')
tense_features.insert(0,("",""))
modus = load_Mode('../ontologies/olia.owl')
modus.insert(0, '') # The first element of the drop-down list should be the empty string
list_cx_uris = load_existing_constructions_uri('cx.ttl')
list_cx = load_existing_constructions_title("cx.ttl")

@app.route('/')
def index():
    return render_template('index.html',
                           uris=uri_list,
                           projects=project_list,
                           semanticroles=semantic_roles,
                           numberfeatures=number_features,
                           casefeatures=case_features,
                           tensefeatures=tense_features,
                           modus=modus,
                           existingconstructions=list_cx)

###################################################
### RETRIEVE INFORMATION FROM THE FORM
###################################################

@app.route('/submit', methods=['POST'])
def submit():
    # Fields in category "Metadata"
    user_name = request.form['uri']
    # Fields in category "General"
    construction_name = request.form['construction']
    construction_name_cleaned = construction_name.replace(" ", "")
    default_research_question_uri = request.form['projectId']
    new_research_question = request.form['Rquestion']
    findings = request.form['findings']
    construction_language = request.form['language']
    # not used for the moment (TODO) construction_status = request.form['construction_status']
    # Fields in category "Meaning of the construction"
    meaning = request.form['meaning']
    image_schema = request.form['new_image_schema']
    # Fields in category "Form-meaning pairings of the elements"
    element_nb = int(request.form['element_nb'])
    descriptions = []
    for i in range(1, element_nb + 1):
        description = request.form[f'morphosyntactic_form_{i}']
        descriptions.append(description)
    # Fields in category "Cotext"
    topics = request.form.getlist('topic_element[]')
    comments = request.form.getlist('comment_element[]')
    focuses = request.form.getlist('focus_element[]')
    backgrounds = request.form.getlist('background_element[]')
    intonation = request.form['intonation']
    gesture = request.form['gesture']
    # Validate incompatible selections (same element as both topic and comment, or focus and background)
    if set(topics) & set(comments):
        return "Error: An element cannot be both Topic and Comment."
    if set(focuses) & set(backgrounds):
        return "Error: An element cannot be both Focus and Background."
    # Fields in category "Links"
    selected_inherits_from_json = request.form['selected_inherits_from']
    if selected_inherits_from_json:
        selected_inherits_from = json.loads(selected_inherits_from_json)
    else:
        selected_inherits_from = []  # Default to an empty list if no data is provided
    selected_inherited_by_json = request.form['selected_inherited_by']
    if selected_inherited_by_json:
        selected_inherited_by = json.loads(selected_inherited_by_json)
    else:
        selected_inherited_by = []  # Default to an empty list if no data is provided
    selected_metaphorical_extension_json = request.form['selected_metaphorical_extension']
    if selected_metaphorical_extension_json:
        selected_metaphorical_extension = json.loads(selected_metaphorical_extension_json)
    else:
        selected_metaphorical_extension = []  # Default to an empty list if no data is provided
    # Research data (only a comment for the moment) TODO
    research_data = request.form['researchdata']
    # Field in the category "Sources"
    reference_rdf = request.form['reference']
    reference_uri = request.form['ReferenceUserItemURI']  # Field for UserItem URI
    literature_entries = request.form.getlist('literature[]')  # Retrieve all literature entries
    url_entries = request.form.getlist('url[]')  # Retrieve all URL entries

###################################################
### CREATE RDF GRAPH
###################################################

    g = Graph()

    cx = Namespace("http://example.org/cx/")
    g.bind("cx", cx)

    membr = Namespace("http://example.org/users/")
    g.bind("membr", membr)

    olia = Namespace("http://purl.org/olia/olia.owl#")
    g.bind("olia", olia)

    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    g.bind("RDFS", RDFS)

    # Triple that defines the URI of the construction
    g.add((cx[construction_name_cleaned], RDF.type, membr.Construction))

###################################################
### IMPLEMENT CONSTRUCTION
###################################################

    # The name of the construction is a concatenation of the language and the title
    construction_complete_title = f"{construction_language} {construction_name}"

    # The research question is the default one if there is no new one indicated
    if new_research_question.strip():
      new_research_question_uri = default_research_question_uri + "_" + datetime.now().strftime("%y%m%d")
      research_question_uri = new_research_question_uri
    else:
      research_question_uri = default_research_question_uri

    g.add((cx[construction_name_cleaned], cx.annotator, membr[user_name]))
    # Add creation date as today.
    g.add((cx[construction_name_cleaned], cx.creationDate, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
    g.add((cx[construction_name_cleaned], cx.hasTitle, Literal(construction_complete_title)))
    g.add((cx[construction_name_cleaned], cx.hasRQ, membr[research_question_uri]))
    if new_research_question.strip():
        g.add((membr[new_research_question_uri], RDF.type, membr.Project))
        g.add((membr[new_research_question_uri], membr.projectName, Literal(new_research_question)))
        g.add((membr[default_research_question_uri], membr.SubProject, membr[new_research_question_uri]))
    if findings.strip():
        g.add((cx[construction_name_cleaned], cx.hasFindings, Literal(findings)))
    else:
        print("No findings to add")
    g.add((cx[construction_name_cleaned], cx.partOfLanguage, Literal(construction_language)))
    if meaning.strip():
        g.add((cx[construction_name_cleaned], cx.hasMeaning, Literal(meaning)))
    else:
        print("No meaning to add")
    if image_schema.strip():
        g.add((cx[construction_name_cleaned], cx.hasImageSchema, Literal(image_schema)))
    else:
        print("No image-schema to add")

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

    # Add triples for topic, comment, focus, and background
    for topic in topics:
        g.add((cx[topic], cx.hasIS, cx.Topic))
    for comment in comments:
        g.add((cx[comment], cx.hasIS, cx.Comment))
    for focus in focuses:
        g.add((cx[focus], cx.hasIS, cx.Focus))
    for background in backgrounds:
        g.add((cx[background], cx.hasIS, cx.Background))

    # Add triples for intonation and gesture
    if intonation.strip():
        g.add((cx[construction_name_cleaned], cx.hasIntonation, Literal(intonation)))
    if gesture.strip():
        g.add((cx[construction_name_cleaned], cx.hasGesture, Literal(gesture)))

    # Add RDF triples for each construction this one inherits from
    for inherit_construction in selected_inherits_from:
        cleaned_inherit_construction = inherit_construction.replace(" ", "")
        g.add((cx[construction_name_cleaned], cx.inheritsFrom, cx[cleaned_inherit_construction]))
        # User can enter the name of a construction that has not been implemented yet
        # When this happens, create a new construction entry, with title, annotator and creation date
        if cleaned_inherit_construction not in list_cx_uris:
            g.add((cx[cleaned_inherit_construction], RDF.type, membr.Construction))
            g.add((cx[cleaned_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[cleaned_inherit_construction], cx.createdOn,
                   Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], cx.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")

    # Add RDF triples for each construction this one is inherited by
    for inherit_construction in selected_inherited_by:
        cleaned_inherit_construction = inherit_construction.replace(" ", "")
        g.add((cx[construction_name_cleaned], cx.inheritedBy, cx[cleaned_inherit_construction]))
        # User can enter the name of a construction that has not been implemented yet
        # When this happens, create a new construction entry, with title, annotator and creation date
        if cleaned_inherit_construction not in list_cx_uris:
            g.add((cx[cleaned_inherit_construction], RDF.type, membr.Construction))
            g.add((cx[cleaned_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[cleaned_inherit_construction], cx.createdOn, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], cx.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")

    # Add RDF triples for each construction this one is metaphorical extension
    for inherit_construction in selected_metaphorical_extension:
        cleaned_inherit_construction = inherit_construction.replace(" ", "")
        g.add((cx[construction_name_cleaned], cx.metaphoricalExtension, cx[cleaned_inherit_construction]))
        # User can enter the name of a construction that has not been implemented yet
        # When this happens, create a new construction entry, with title, annotator and creation date
        if cleaned_inherit_construction not in list_cx_uris:
            g.add((cx[cleaned_inherit_construction], RDF.type, membr.Construction))
            g.add((cx[cleaned_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[cleaned_inherit_construction], cx.createdOn,
                       Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], cx.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")

    # Add a comment about research data:
    if research_data.strip():
        g.add((cx[construction_name_cleaned], RDFS.comment, Literal(research_data)))

    # Add each URL from other constructicons (with rdfs:seeAlso)
    for url in url_entries:
        if url:  # Only process non-empty entries
            g.add((cx[construction_name_cleaned], RDFS.seeAlso, URIRef(url)))

###################################################
### IMPLEMENT SLOTS
###################################################

    #A loop that adds the value of the fields related to the slots for each slot.
    for i in range(1, element_nb + 1):
        y = i -1
        element_uri = URIRef(cx[f"{construction_name_cleaned}_{chr(65 + y)}"])
        # Define element/slot as belonging to a subclass of the "Slot" class,
        # either by being a non-optional slot (SlotMandatory) or an optional slot (SlotOptional).
        optionality = request.form[f'optionality_{i}']
        if optionality == "non-optional":
            optionality_uri = "SlotMandatory"
        else:
            optionality_uri = "SlotOptional"
        g.add((element_uri, RDF.type, cx[optionality_uri]))
        # If defined, attribute its morphosyntactic form, word order specification, translation, syntactic function,
        # semantic contribution, animacy, gender, number, case, person, tense, mode, voice, root, stem
        # to the element/slot.
        morphosyntactic_form = request.form[f'morphosyntactic_form_{i}']
        if morphosyntactic_form.strip():
          g.add((element_uri, cx.hasSyntacticForm, Literal(morphosyntactic_form)))
        word_order = request.form[f'WordOrder_{i}']
        if word_order.strip():
            g.add((element_uri, cx.WordOrder, Literal(word_order)))
        translation = request.form[f'translation_{i}']
        if translation.strip():
            g.add((element_uri, cx.hasTranslation, Literal(translation)))
        syntactic_function = request.form[f'syntactic_function_{i}']
        if syntactic_function.strip():
            g.add((element_uri, cx.hasSyntacticFunction, Literal(syntactic_function)))
        semantic_contribution = request.form[f'semantic_contribution_{i}']
        if semantic_contribution.strip():
            semantic_contribution = semantic_contribution + "Role"
            g.add((element_uri, cx.hasSemanticContribution, olia[semantic_contribution]))
        else:
            add_semantic_contribution = request.form[f'add_semantic_contribution_{i}']
            if add_semantic_contribution.strip():
                print("Warning: new semantic contribution!")
                g.add((element_uri, cx.hasSemanticContribution, Literal(add_semantic_contribution)))
        other_animacy = request.form[f'other_animacy_{i}']
        if other_animacy.strip():
            print("Warning: new value for animacy!")
            g.add((element_uri, cx.hasAnimacy, Literal(other_animacy)))
        else:
            animacy = request.form[f'animacy_{i}']
            if animacy.strip():
                g.add((element_uri, cx.hasAnimacy, cx[animacy]))
        other_gender = request.form[f'other_gender_{i}']
        if other_gender.strip():
            print("Warning: new value for gender!")
            g.add((element_uri, cx.hasGender, Literal(other_gender)))
        else:
            gender = request.form[f'gender_{i}']
            if gender.strip():
                g.add((element_uri, cx.hasGender, cx[gender]))
        number = request.form[f'number_{i}']
        if number.strip():
            g.add((element_uri, cx.hasNumberFeature, olia[number]))
        else:
            add_number = request.form[f'add_number_{i}']
            if add_number.strip():
                print("Warning: new value for number!")
                g.add((element_uri, cx.hasNumberFeature, Literal(add_number)))
        case = request.form[f'case_{i}']
        if case.strip():
            case = case + "Case"
            g.add((element_uri, cx.hasCaseFeature, olia[case]))
        else:
            add_case = request.form[f'add_case_{i}']
            if add_case.strip():
                print("Warning: new value for case!")
                g.add((element_uri, cx.hasCaseFeature, Literal(add_case)))
        other_person = request.form[f'other_person_{i}']
        if other_person.strip():
            print("Warning: new value for person!")
            g.add((element_uri, cx.hasPerson, Literal(other_person)))
        else:
            person = request.form[f'person_{i}']
            if person.strip():
                g.add((element_uri, cx.hasPerson, cx[person]))
        tense_uri = request.form[f'tense_{i}']
        if tense_uri.strip():
            g.add((element_uri, cx.hasTenseFeature, URIRef(tense_uri))) # We need to use URIRef here because the prefix will be sometimes olia and sometimes oliatop
        else:
            add_tense = request.form[f'add_tense_{i}']
            if add_tense.strip():
                print("Warning: new value for tense!")
                g.add((element_uri, cx.hasTenseFeature, Literal(add_tense)))
        modus = request.form[f'modus_{i}']
        if modus.strip():
            modus = modus + "Verb"
            g.add((element_uri, cx.hasMode, olia[modus]))
        else:
            add_modus = request.form[f'add_modus_{i}']
            if add_modus.strip():
                print("Warning: new value for mode!")
                g.add((element_uri, cx.hasMode, Literal(add_modus)))
        other_voice = request.form[f'other_voice_{i}']
        if other_voice.strip():
            print("Warning: new value for voice!")
            g.add((element_uri, cx.hasVoice, Literal(other_voice)))
        else:
            voice = request.form[f'voice_{i}']
            if voice.strip():
                g.add((element_uri, cx.hasVoice, cx[voice]))
        root = request.form[f'root_{i}']
        if root.strip():
            g.add((element_uri, cx.hasRoot, Literal(root)))
        stem = request.form[f'stem_{i}']
        if stem.strip():
            g.add((element_uri, cx.hasStem, Literal(stem)))
        semantic_property = request.form[f'semprop_{i}']
        if semantic_property.strip():
            g.add((element_uri, cx.hasSemanticProperty, Literal(semantic_property)))
        other_element_specification = request.form[f'element_specification_{i}']
        if other_element_specification.strip():
            g.add((element_uri, RDFS.comment, Literal(other_element_specification)))

    # Parse and merge the RDF code from the 'Reference' field
    if reference_rdf:
            try:
                reference_graph = Graph()
                reference_graph.parse(data=reference_rdf, format='xml')  # Assuming RDF/XML format
                # Extract the subject (URI) from the 'Reference' field
                reference_subjects = list(reference_graph.subjects())
                if reference_subjects:
                    reference_subject = reference_subjects[0]  # Assuming the first subject is the main reference
                    g.add((cx[construction_name_cleaned], cx.basedOn, reference_subject))
                g += reference_graph  # Merge with the existing graph
            except Exception as e:
                return f"Error parsing RDF Reference: {e}", 400

    # Parse and merge all Literature RDF entries
    for literature_rdf in literature_entries:
            if literature_rdf:  # Only process non-empty entries
                try:
                    literature_graph = Graph()
                    literature_graph.parse(data=literature_rdf, format='xml')  # Assuming RDF/XML format
                    # Extract the subject (URI) from each 'Literature' entry
                    literature_subjects = list(literature_graph.subjects())
                    if literature_subjects:
                        literature_subject = literature_subjects[0]
                        g.add((cx[construction_name_cleaned], cx.hasLiterature, literature_subject))
                    g += literature_graph  # Merge with the existing graph
                except Exception as e:
                    return f"Error parsing RDF Literature: {e}",

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
        g.add((example_uri, cx.hasText, Literal(example_text)))
        g.add((example_uri, cx.hasTranslation, Literal(translation)))
        g.add((example_uri, cx.hasGlosses, Literal(glosses)))
        g.add((example_uri, RDFS.comment, Literal(comment)))

        example_counter += 1

###################################################
### SERIALIZE THE RDF GRAPH TO A .ttl FILE
###################################################

    file_path = f'{user_name.split("/")[-1]}_cx.ttl'
    g.serialize(destination=file_path, format='turtle')

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
