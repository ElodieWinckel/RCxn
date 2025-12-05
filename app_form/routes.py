from . import app_form_blueprint
from flask import current_app, request, render_template, send_file
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from datetime import datetime
import re
import glob
import json
import os

# Check if the production directory exists
if os.path.exists("/data/www/RCxn"):
    os.chdir("/data/www/RCxn")  # # Set the working directory to the application's production path

###################################################
### FUNCTIONS REQUIRED TO EXTRACT FROM DATABASES AND ONTOLOGIES
###################################################

# Load URIs and family names from existing database of researchers (users.ttl)
def load_user_names_from_ttl(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    foaf = Namespace('http://xmlns.com/foaf/0.1/')
    uris_and_names = [(str(s).replace("http://example.org/users#", ""),
                       str(g.value(s, foaf.familyName))) for s in g.subjects(RDF.type, foaf.Person)]
    return uris_and_names

# Load URIs and project names from existing database of research projects (users.ttl)
def load_projects_from_ttl(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
    foaf = Namespace("http://xmlns.com/foaf/0.1/")
    project_list = []
    for project in g.subjects(RDF.type, rsrch.Project):
        uri = str(project).replace("http://example.org/users#", "")
        title = str(g.value(project, rsrch.projectName))
        project_list.append((uri, title))
    return project_list

# Load URIs and finding labels from existing database of research projects (users.ttl)
def load_findings_from_ttl(file_path):
    g = Graph()
    g.parse(file_path, format='turtle')
    rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    uris_and_names = [(str(s).replace("http://example.org/users#", ""),
                       str(g.value(s, RDFS.label))) for s in g.subjects(RDF.type, rsrch.Finding)]
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
    #g.parse("http://purl.org/olia/olia-top.owl#", format='xml') #TODO: cases are not found, but no error message
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

# Load URIs and title of already existing constructions
def load_existing_constructions(file_path):
    g = Graph()
    for ttl_file in glob.glob(file_path):
        g.parse(ttl_file, format="turtle")
    g.parse("ontologies/lg.rdf", format="xml")
    constructions = []

    # SPARQL query to get the title for each construction
    query = """
        PREFIX rcxn: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#>
        PREFIX lg: <https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?construction ?title ?lang
        WHERE {
            ?construction a rcxn:Construction .
            ?construction rcxn:hasTitle ?title .
            ?construction lg:partOfLanguage ?code .
            ?code rdfs:label ?lang .
        }
        """

    # Execute the SPARQL query
    results = g.query(query)

    # Process query results
    for row in results:
        construction_uri = str(row.construction).replace("http://example.org/cx/", "")
        title = str(row.title)
        lang = str(row.lang)

        # Append construction details as dictionary
        constructions.append({
            'uri': construction_uri,
            'title': title + " [" + lang + "]"
        })
    return constructions

def get_metalanguage(lang_uri):
    """
    Walks up the isVarietyOf chain until it finds
    the top-level 'metalanguage' (no parent).
    """
    ontology_lg = Graph() # Create graph
    ontology_lg.parse("ontologies/lg.rdf", format="xml") # Load the ontology for languages into the graph
    lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
    ontology_lg.bind("lg", lg)
    current = lang_uri
    visited = set()  # to avoid infinite loops if bad data
    while True:
        parents = list(ontology_lg.objects(subject=current, predicate=lg.isVarietyOf))
        if not parents:
            # no further parent, return current as the metalanguage
            return current
        parent = parents[0]
        if parent in visited:
            # cycle detected
            return current
        visited.add(parent)
        current = parent

###################################################
### RUN HTML FORM
###################################################

# Prepare all lists that are passed to the HTML form
# /data/www/RCxn/
uri_list = load_user_names_from_ttl('Abox/users.ttl')
project_list = load_projects_from_ttl('Abox/users.ttl')
findings_list = load_findings_from_ttl('Abox/users.ttl')
semantic_roles = load_SemanticRoles('ontologies/olia.owl')
semantic_roles.insert(0, '') # The first element of the drop-down list should be the empty string
number_features = load_NumberFeatures('ontologies/olia.owl')
number_features.insert(0, '') # The first element of the drop-down list should be the empty string
case_features = load_CaseFeatures('ontologies/olia.owl')
case_features.insert(0, '') # The first element of the drop-down list should be the empty string
tense_features = load_TenseFeatures('ontologies/olia.owl')
tense_features.insert(0,("",""))
modus = load_Mode('ontologies/olia.owl')
modus.insert(0, '') # The first element of the drop-down list should be the empty string
list_cx = load_existing_constructions("instance/Submissions/*_cx.ttl")
list_cx_titles = [entry["title"] for entry in list_cx] # list with only titles of Constructions already in the constructicon
list_cx_titles.sort(key=lambda x: x.lower())

@app_form_blueprint.route('/')
def online_form():
    return render_template('app_form/form.html',
                           uris=uri_list,
                           projects=project_list,
                           findings=findings_list,
                           semanticroles=semantic_roles,
                           numberfeatures=number_features,
                           casefeatures=case_features,
                           tensefeatures=tense_features,
                           modus=modus,
                           existingconstructions=list_cx_titles)

###################################################
### RETRIEVE INFORMATION FROM THE FORM
###################################################

@app_form_blueprint.route('/submit', methods=['POST'])
def form_submit():
    # Fields in category "Metadata"
    user_name = request.form['uri']
    # Fields in category "General"
    construction_language_uri = request.form['language']  # the URI
    # construction_language = request.form['language_label']  # the label, no use for the moment
    construction_name = request.form['construction']
    construction_name_cleaned = construction_language_uri + "_" + construction_name.replace(" ", "")
    default_research_question_uri = request.form['projectId']
    new_research_question = request.form['Rquestion']
    findingsId = request.form['findingsId'] # Flask receives either: (a) The selected findingsId if an existing finding is chosen,
    findings = request.form['findings'] # or (b) the manually entered text from findings if "Create new findings" is selected.
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

    membr = Namespace("http://example.org/users#")
    g.bind("membr", membr)

    rcxn = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#")
    g.bind("rcxn", rcxn)

    rsrch = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#")
    g.bind("rsrch", rsrch)

    links = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/links-1.0#")
    g.bind("links", links)

    foaf = Namespace("http://xmlns.com/foaf/0.1/")
    g.bind("foaf", foaf)

    olia = Namespace("http://purl.org/olia/olia.owl#")
    g.bind("olia", olia)

    oliatop = Namespace("http://purl.org/olia/olia-top.owl#")
    g.bind("oliatop", oliatop)

    RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    g.bind("RDFS", RDFS)

    lg = Namespace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#")
    g.bind("lg", lg)

    # Triple that defines the URI of the construction
    g.add((cx[construction_name_cleaned], RDF.type, rcxn.Construction))

###################################################
### IMPLEMENT CONSTRUCTION METADATA
###################################################

    # URI for Metadata
    metadata_uri = f"{construction_name_cleaned}_MD"
    g.add((cx[metadata_uri], RDF.type, rcxn.Metadata))
    # Triple to relate cx to its metadata
    g.add((cx[construction_name_cleaned], rcxn.hasMetadata, cx[metadata_uri]))

    # ANNOTATOR
    g.add((cx[metadata_uri], cx.annotator, membr[user_name]))

    # CREATION DATA
    # Add creation date as today.
    g.add((cx[metadata_uri], rcxn.creationDate, Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))

    # RESEARCH QUESTION
    # Triples needed if new research question has been added by user
    if new_research_question.strip():
        new_research_question_uri = default_research_question_uri + "_" + datetime.now().strftime("%y%m%d%H%M")
        g.add((membr[new_research_question_uri], RDF.type, rsrch.Project))
        g.add((membr[new_research_question_uri], rsrch.projectName, Literal(new_research_question)))
        g.add((membr[user_name], foaf.currentProject, membr[new_research_question_uri]))
        g.add((membr[default_research_question_uri], rsrch.hasResearchQuestion, membr[new_research_question_uri]))
        current_research_question = new_research_question_uri
    else:
        current_research_question = default_research_question_uri

    # FINDINGS
    if findingsId.strip() and findingsId != "new": # first check if an already existing finding was used
                            # NB: Important to do it first, since some "new finding" could be stored in cache.
        g.add((membr[findingsId], rsrch.basedOn, cx[construction_name_cleaned]))
    else: # otherwise use new finding
        new_finding = current_research_question + "_F" + datetime.now().strftime("%y%m%d%H%M")
        g.add((membr[current_research_question], rsrch.hasFindings, membr[new_finding]))
        g.add((membr[new_finding], RDF.type, rsrch.Finding))
        g.add((membr[new_finding], RDFS.label, Literal(findings)))
        g.add((membr[new_finding], rsrch.basedOn, cx[construction_name_cleaned]))

    # TITLE
    construction_complete_title = f"{construction_name}"
    g.add((cx[construction_name_cleaned], rcxn.hasTitle, Literal(construction_complete_title)))

###################################################
### IMPLEMENT CONSTRUCTION SOURCES
###################################################

    # URI for Sources
    sources_uri = f"{construction_name_cleaned}_Sources"

    # REFERENCE
    # Parse and merge the RDF code from the 'Reference' field
    if reference_rdf:
            try:
                reference_graph = Graph()
                reference_graph.parse(data=reference_rdf, format='xml')  # Assuming RDF/XML format
                # Extract the subject (URI) from the 'Reference' field
                reference_subjects = list(reference_graph.subjects())
                if reference_subjects:
                    reference_subject = reference_subjects[0]  # Assuming the first subject is the main reference
                    # Define sources uri
                    g.add((cx[sources_uri], RDF.type,
                           cx.Collection))  # TODO Collection (or similar) might already exist in dc
                    # Triple to relate sources to metadata
                    g.add((cx[metadata_uri], cx.hasSources, cx[sources_uri]))
                    # Triple for reference
                    g.add((cx[sources_uri], cx.basedOn, reference_subject)) # TODO basedOn already exists to relate a finding to a construction or to research data, find another name
                g += reference_graph  # Merge with the existing graph
            except Exception as e:
                return f"Error parsing RDF Reference: {e}", 400

    # LITERATURE
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
                        # Define sources uri
                        g.add((cx[sources_uri], RDF.type,
                               cx.Collection))  # TODO Collection (or similar) might already exist in dc
                        # Triple to relate sources to metadata
                        g.add((cx[metadata_uri], cx.hasSources, cx[sources_uri]))
                        # Triple for Literature
                        g.add((cx[sources_uri], cx.hasLiterature, literature_subject))
                    g += literature_graph  # Merge with the existing graph
                except Exception as e:
                    return f"Error parsing RDF Literature: {e}",

    # OTHER CONSTRUCTICONS
    # Add each URL from other constructicons (with rdfs:seeAlso)
    for url in url_entries:
        if url:  # Only process non-empty entries
            # Define sources uri
            g.add((cx[sources_uri], RDF.type, cx.Collection))  # TODO Collection (or similar) might already exist in dc
            # Triple to relate sources to metadata
            g.add((cx[metadata_uri], cx.hasSources, cx[sources_uri]))
            # Triple for URL from another constructicon
            g.add((cx[sources_uri], RDFS.seeAlso, URIRef(url)))

###################################################
### IMPLEMENT CONSTRUCTION LANGUAGE
###################################################

    g.add((cx[construction_name_cleaned], lg.partOfLanguage, lg[construction_language_uri]))
    metalanguage_uri = get_metalanguage(lg[construction_language_uri]) # full URI of metalanguage associated with this language
    metalanguage_code = str(metalanguage_uri).replace("https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#", "")

    ###################################################
### IMPLEMENT CONSTRUCTION MEANING
###################################################

    # URI for Construction Meaning
    cx_meaning_uri = f"{construction_name_cleaned}_Meaning"
    g.add((cx[cx_meaning_uri], RDF.type, rcxn.ConstructionMeaning))
    # Triple to relate cx to it meaning
    g.add((cx[construction_name_cleaned], rcxn.hasConstructionMeaning, cx[cx_meaning_uri]))

    # MEANING (GENERAL)
    if meaning.strip():
        g.add((cx[cx_meaning_uri], rcxn.hasMeaning, Literal(meaning)))
    else:
        print("No meaning to add")

    # IMAGE SCHEMA
    if image_schema.strip():
        g.add((cx[cx_meaning_uri], rcxn.usesImageSchema, Literal(image_schema)))
    else:
        print("No image-schema to add")

###################################################
### IMPLEMENT CONSTRUCTION ELEMENTS (AKA SLOTS)
###################################################

    #Create the sequence of construction elements
    ## Create a new blank node for the sequence
    seq_slots = URIRef(cx[f"{construction_name_cleaned}_slots"])
    g.add((seq_slots, RDF.type, RDF.Seq))
    # Add elements to the sequence
    for i in range(element_nb):
        element_uri = cx[f"{construction_name_cleaned}_{i + 1}"]
        seq_position = URIRef(RDF[f"_{i + 1}"])
        g.add((seq_slots, seq_position, element_uri))
    ## Add the sequence as the object of the triple
    g.add((cx[construction_name_cleaned], rcxn.hasSlots, seq_slots))

    # FROM NOW ON: A LOOP THAT ADDS THE VALUE OF THE FIELDS RELATED TO THE SLOTS FOR EACH SLOT
    for i in range(1, element_nb + 1):
        y = i -1
        element_uri = cx[f"{construction_name_cleaned}_{i}"]

        # Retrieve information from the form
        phonology = request.form[f'phonology_{i}']
        semantic_contribution = request.form[f'semantic_contribution_{i}']
        semantic_property = request.form[f'semprop_{i}']
        colloprofile = request.form[f'colloprofile_{i}']
        other_animacy = request.form[f'other_animacy_{i}']
        animacy = request.form[f'animacy_{i}']
        other_gender = request.form[f'other_gender_{i}']
        gender = request.form[f'gender_{i}']
        number = request.form[f'number_{i}']
        add_number = request.form[f'add_number_{i}']
        other_person = request.form[f'other_person_{i}']
        person = request.form[f'person_{i}']
        tense_uri = request.form[f'tense_{i}']
        add_tense = request.form[f'add_tense_{i}']
        modus = request.form[f'modus_{i}']
        add_modus = request.form[f'add_modus_{i}']
        other_voice = request.form[f'other_voice_{i}']
        voice = request.form[f'voice_{i}']
        morphosyntactic_form_json = request.form.get(f"morphosyntactic_form_{i}", "[]")
        try:
            morphosyntactic_form = json.loads(morphosyntactic_form_json)
        except json.JSONDecodeError:
            morphosyntactic_form = []
        word_order = request.form[f'WordOrder_{i}']
        surface = request.form[f'surface_form_{i}']
        transliteration = request.form[f'transliteration_{i}']
        translation = request.form[f'translation_{i}']
        syntactic_function = request.form[f'syntactic_function_{i}']
        case = request.form[f'case_{i}']
        add_case = request.form[f'add_case_{i}']
        root = request.form[f'root_{i}']
        stem = request.form[f'stem_{i}']
        add_semantic_contribution = request.form[f'add_semantic_contribution_{i}']
        other_element_specification = request.form[f'element_specification_{i}']

        # Define element/slot as belonging to a subclass of the "Slot" class,
        # either by being a non-optional slot (SlotMandatory) or an optional slot (SlotOptional).
        optionality = request.form[f'optionality_{i}']
        if optionality == "non-optional":
            optionality_uri = "SlotMandatory"
        else:
            optionality_uri = "SlotOptional"
        g.add((element_uri, RDF.type, rcxn[optionality_uri]))

        # If defined, add info about word order
        # TODO ultimately, we want to implement it differently (with before, precedes, etc.)
        if word_order.strip():
            g.add((element_uri, cx.WordOrder, Literal(word_order)))

        # Add a comment for collocation and any "other element specification" defined by user
        if other_element_specification.strip():
            g.add((element_uri, RDFS.comment, Literal(other_element_specification)))
        if colloprofile.strip():
            g.add((element_uri, RDFS.comment, Literal("colloprofile: "+colloprofile)))

        # If defined, attribute its semantic contribution and semantic property to the element/slot
        # (i.e., all meaning info except index)
        if add_semantic_contribution.strip():
            g.add((element_uri, rcxn.hasOtherSemanticContribution, Literal(add_semantic_contribution)))
        else:
            if semantic_contribution.strip():
                semantic_contribution = semantic_contribution + "Role"
                g.add((element_uri, rcxn.hasSemanticRole, oliatop[semantic_contribution]))
        if semantic_property.strip():
            g.add((element_uri, rcxn.hasSemanticProperty, Literal(semantic_property)))

        # URI for Slot Index
        index_uri = cx[f"{construction_name_cleaned}_{i}_Index"]
        # Triple to relate index to meaning
        if other_animacy.strip() or animacy.strip() or other_gender.strip() or gender.strip() or person.strip() or tense_uri.strip() or add_tense.strip() or modus.strip() or add_modus.strip() or other_voice.strip() or voice.strip():
            g.add((element_uri, cx.hasIndex, index_uri))

        # If defined, attribute its animacy, gender, number, person, tense, mode, voice to the element/slot index
        # If the index has animacy or gender, it refers to an individual (subtype of index)
        # If the index has tense, mode or voice, it refers to an event (subtype of index)
        if other_animacy.strip():
            print("Warning: new value for animacy!")
            g.add((index_uri, cx.hasAnimacy, Literal(other_animacy)))
            g.add((index_uri, RDF.type, cx.Individual))
        else:
            if animacy.strip():
                g.add((index_uri, cx.hasAnimacy, cx[animacy]))
                g.add((index_uri, RDF.type, cx.Individual))
        if other_gender.strip():
            print("Warning: new value for gender!")
            g.add((index_uri, cx.hasGender, Literal(other_gender)))
            g.add((index_uri, RDF.type, cx.Individual))
        else:
            if gender.strip():
                g.add((index_uri, cx.hasGender, cx[gender]))
                g.add((index_uri, RDF.type, cx.Individual))
        if number.strip():
            g.add((index_uri, olia.hasNumber, olia[number]))
        else:
            if add_number.strip():
                print("Warning: new value for number!")
                g.add((index_uri, olia.hasNumber, Literal(add_number)))
        if other_person.strip():
            print("Warning: new value for person!")
            g.add((index_uri, cx.hasPerson, Literal(other_person)))
        else:
            if person.strip():
                g.add((index_uri, cx.hasPerson, cx[person]))
        if add_tense.strip():
            print("Warning: new value for tense!")
            g.add((index_uri, olia.hasTense, Literal(add_tense)))
            g.add((index_uri, RDF.type, cx.Event))
        else:
            if tense_uri.strip():
                g.add((index_uri, olia.hasTense, URIRef(tense_uri)))  # We need to use URIRef here because the prefix will be sometimes olia and sometimes oliatop
                g.add((index_uri, RDF.type, cx.Event))
        if add_modus.strip():
            print("Warning: new value for mode!")
            g.add((index_uri, cx.hasMode, Literal(add_modus)))
            g.add((index_uri, RDF.type, cx.Event))
        else:
            if modus.strip():
                modus = modus + "Verb"
                g.add((index_uri, cx.hasMode, olia[modus]))
                g.add((index_uri, RDF.type, cx.Event))
        if other_voice.strip():
            print("Warning: new value for voice!")
            g.add((index_uri, cx.hasVoice, Literal(other_voice)))
            g.add((index_uri, RDF.type, cx.Event))
        else:
            if voice.strip():
                g.add((index_uri, cx.hasVoice, cx[voice]))
                g.add((index_uri, RDF.type, cx.Event))

        # URI for Slot Form
        slot_form_uri = cx[f"{construction_name_cleaned}_{i}_Form"]
        # Triple to relate slot to it meaning (if needed)
        if morphosyntactic_form or phonology.strip() or root.strip() or stem.strip() or surface.strip():
            g.add((element_uri, rcxn.hasSlotForm, slot_form_uri))
            g.add((slot_form_uri, RDF.type, rcxn.SlotForm))

        # Formal aspects attributed to the URI for element/slot form
        if phonology.strip():
            g.add((slot_form_uri, rcxn.hasPhonology, Literal(phonology)))
        if root.strip():
            g.add((slot_form_uri, rcxn.hasRoot, Literal(root)))
        if stem.strip():
            g.add((slot_form_uri, rcxn.hasStem, Literal(stem)))
        if surface.strip():
            g.add((slot_form_uri, rcxn.hasSurfaceForm, Literal(surface)))
        if translation.strip():
            g.add((element_uri, cx.hasTranslation, Literal(translation)))
        if transliteration.strip():
            g.add((element_uri, cx.hasTransliteration, Literal(transliteration)))
        if morphosyntactic_form:
            for morphosyn in morphosyntactic_form:
                # Users can select a construction already in the constructicon
                # When this happens, the uri has to be identified
                if morphosyn in {entry['title'] for entry in list_cx}:
                    cleaned_morphosyn_construction = next(
                        (entry['uri'] for entry in list_cx if entry['title'] == morphosyn),
                        None  # Default if not found
                    )
                else:  # Users can also enter the name of a construction that has not been implemented yet
                    # When this happens, create a new construction entry, with title, annotator and creation date
                    cleaned_morphosyn_construction = morphosyn.replace(" ", "")
                    metadata_morphosyn_construction = f"{cleaned_morphosyn_construction}_MD"
                    g.add((cx[cleaned_morphosyn_construction], RDF.type, rcxn.Construction))
                    g.add((cx[cleaned_morphosyn_construction], rcxn.hasMetadata, cx[metadata_morphosyn_construction]))
                    g.add((cx[metadata_morphosyn_construction], RDF.type, rcxn.Metadata))
                    g.add((cx[metadata_morphosyn_construction], cx.annotator, membr[user_name]))
                    g.add((cx[metadata_morphosyn_construction], rcxn.creationDate,
                           Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
                    g.add((cx[cleaned_morphosyn_construction], rcxn.hasTitle, Literal(morphosyn)))
                    print("New construction needed!")
                # In any case, write a triplet defining this construction the object of hasSyntacticForm, and a triplet for the corresponding link
                g.add((slot_form_uri, rcxn.hasSyntacticForm, cx[cleaned_morphosyn_construction]))
                g.add((cx[cleaned_morphosyn_construction], rcxn.elementOf, cx[construction_name_cleaned]))

        # If defined, attribute its syntactic function and case to the element/slot.
        if syntactic_function.strip():
            g.add((element_uri, rcxn.hasSyntacticFunction, Literal(syntactic_function)))
        if add_case.strip():
            print("Warning: new value for case!")
            g.add((element_uri, cx.hasCaseFeature, Literal(add_case)))
        else:
            if case.strip():
                case = case + "Case"
                g.add((element_uri, cx.hasCaseFeature, olia[case]))

###################################################
### IMPLEMENT CONSTRUCTION COTEXT
###################################################

    # INFORMATION STRUCTURE #TODO: For the moment, each slot gets an IS; maybe we want the cx to have an IS instead
    for topic in topics:
        g.add((cx[topic], cx.hasIS, cx.Topic))
    for comment in comments:
        g.add((cx[comment], cx.hasIS, cx.Comment))
    for focus in focuses:
        g.add((cx[focus], cx.hasIS, cx.Focus))
    for background in backgrounds:
        g.add((cx[background], cx.hasIS, cx.Background))

    # INTONATION #TODO
    if intonation.strip():
        g.add((cx[construction_name_cleaned], cx.hasIntonation, Literal(intonation)))

    # GESTURE #TODO
    if gesture.strip():
        g.add((cx[construction_name_cleaned], cx.hasGesture, Literal(gesture)))

###################################################
### IMPLEMENT LINKS BETWEEN CONSTRUCTIONS
###################################################

    # Add RDF triples for each construction this one inherits from
    for inherit_construction in selected_inherits_from:
        # Users can select a construction already in the constructicon
        # When this happens, the uri has to be identified
        if inherit_construction in {entry['title'] for entry in list_cx}:
            cleaned_inherit_construction = next(
                (entry['uri'] for entry in list_cx if entry['title'] == inherit_construction),
                None  # Default if not found
            )
        else: # Users can also enter the name of a construction that has not been implemented yet
            # When this happens, create a new construction entry, with title, annotator and creation date
            cleaned_inherit_construction = inherit_construction.replace(" ", "")
            metadata_inherit_construction = f"{cleaned_inherit_construction}_MD"
            g.add((cx[cleaned_inherit_construction], RDF.type, rcxn.Construction))
            g.add((cx[cleaned_inherit_construction], rcxn.hasMetadata, cx[metadata_inherit_construction]))
            g.add((cx[metadata_inherit_construction], RDF.type, rcxn.Metadata))
            g.add((cx[metadata_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[metadata_inherit_construction], rcxn.creationDate,
                   Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], rcxn.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")
        # In any case, write a triplet defining this construction as inherited from (and inverse link)
        g.add((cx[construction_name_cleaned], links.inheritsFrom, cx[cleaned_inherit_construction]))
        g.add((cx[cleaned_inherit_construction], links.inheritedBy, cx[construction_name_cleaned]))

    # Add RDF triples for each construction this one is inherited by
    for inherit_construction in selected_inherited_by:
        # Users can select a construction already in the constructicon
        # When this happens, the uri has to be identified
        if inherit_construction in {entry['title'] for entry in list_cx}:
            cleaned_inherit_construction = next(
                (entry['uri'] for entry in list_cx if entry['title'] == inherit_construction),
                None  # Default if not found
            )
        else:  # Users can also enter the name of a construction that has not been implemented yet
            # When this happens, create a new construction entry, with title, annotator and creation date
            cleaned_inherit_construction = inherit_construction.replace(" ", "")
            metadata_inherit_construction = f"{cleaned_inherit_construction}_MD"
            g.add((cx[cleaned_inherit_construction], RDF.type, rcxn.Construction))
            g.add((cx[cleaned_inherit_construction], rcxn.hasMetadata, cx[metadata_inherit_construction]))
            g.add((cx[metadata_inherit_construction], RDF.type, rcxn.Metadata))
            g.add((cx[metadata_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[metadata_inherit_construction], rcxn.creationDate,
                   Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], rcxn.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")
        # In any case, write a triplet defining this construction as inherited from
        g.add((cx[construction_name_cleaned], links.inheritedBy, cx[cleaned_inherit_construction]))
        g.add((cx[cleaned_inherit_construction], links.inheritsFrom, cx[construction_name_cleaned]))

    # Add RDF triples for each construction this one is metaphorical extension of
    for inherit_construction in selected_metaphorical_extension:
        # Users can select a construction already in the constructicon
        # When this happens, the uri has to be identified
        if inherit_construction in {entry['title'] for entry in list_cx}:
            cleaned_inherit_construction = next(
                (entry['uri'] for entry in list_cx if entry['title'] == inherit_construction),
                None  # Default if not found
            )
        else:  # Users can also enter the name of a construction that has not been implemented yet
            # When this happens, create a new construction entry, with title, annotator and creation date
            cleaned_inherit_construction = str(metalanguage_code) + "_" + inherit_construction.replace(" ", "")
            metadata_inherit_construction = f"{cleaned_inherit_construction}_MD"
            g.add((cx[cleaned_inherit_construction], RDF.type, rcxn.Construction))
            g.add((cx[cleaned_inherit_construction], rcxn.hasMetadata, cx[metadata_inherit_construction]))
            g.add((cx[cleaned_inherit_construction], lg.partOfLanguage, metalanguage_uri)) # A metaphorical extension belong automatically to the same (meta-)language
            g.add((cx[metadata_inherit_construction], RDF.type, rcxn.Metadata))
            g.add((cx[metadata_inherit_construction], cx.annotator, membr[user_name]))
            g.add((cx[metadata_inherit_construction], rcxn.creationDate,
                   Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
            g.add((cx[cleaned_inherit_construction], rcxn.hasTitle, Literal(inherit_construction)))
            print("New construction needed!")
        # In any case, write a triplet defining this construction as inherited from
        g.add((cx[construction_name_cleaned], links.metaphoricalLink, cx[cleaned_inherit_construction]))

    # Handle the dynamically added similarity links
    similarity_counter = 1
    while f'similarityLink_Cx_{similarity_counter}' in request.form:
        # Fetch values for each similarity link
        similarity_link = request.form[f'similarityLink_Cx_{similarity_counter}'] # name of the construction
        similarity_link_crossl = request.form[f'crosslinguistic_{similarity_counter}'] # whether the link is cross-linguistic
        similarity_link_meaning = request.form[f'meaningSim_{similarity_counter}'] # type of meaning link
        similarity_link_form = request.form[f'formSim_{similarity_counter}'] # type of form link
        # Add RDF triples for the syntactic link
        if similarity_link.strip():
            # Identify the URI of the property
            if similarity_link_crossl == "Empty" or similarity_link_meaning == "Empty" or similarity_link_form == "Empty":
                return "Error: You haven't specified all properties of a similarity link."
            if similarity_link_crossl == "yes":
                uri = f"CL_{similarity_link_form}Form{similarity_link_meaning}Function"
            else:
                uri = f"{similarity_link_form}Form{similarity_link_meaning}Function"
            property_uri = URIRef(links[uri])
            # Users can select a construction already in the constructicon
            # When this happens, the uri has to be identified
            if similarity_link in {entry['title'] for entry in list_cx}:
                cleaned_inherit_construction = next(
                    (entry['uri'] for entry in list_cx if entry['title'] == similarity_link),
                    None  # Default if not found
                )
            else:  # Users can also enter the name of a construction that has not been implemented yet
                # When this happens, create a new construction entry, with title, annotator and creation date
                cleaned_inherit_construction = similarity_link.replace(" ", "")
                metadata_inherit_construction = f"{cleaned_inherit_construction}_MD"
                g.add((cx[cleaned_inherit_construction], RDF.type, rcxn.Construction))
                g.add((cx[cleaned_inherit_construction], rcxn.hasMetadata, cx[metadata_inherit_construction]))
                g.add((cx[metadata_inherit_construction], RDF.type, rcxn.Metadata))
                g.add((cx[metadata_inherit_construction], cx.annotator, membr[user_name]))
                g.add((cx[metadata_inherit_construction], rcxn.creationDate,
                       Literal(datetime.now().strftime('%Y-%m-%d'), datatype=XSD.date)))
                g.add((cx[cleaned_inherit_construction], rcxn.hasTitle, Literal(similarity_link)))
                print("New construction needed!")
            # In any case, write a triplet defining this construction as having similarity link (and inverse link)
            g.add((cx[construction_name_cleaned], property_uri, cx[cleaned_inherit_construction]))
            g.add((cx[cleaned_inherit_construction], property_uri, cx[construction_name_cleaned]))

        similarity_counter += 1

###################################################
### IMPLEMENT EXAMPLES
###################################################

    # Handle the dynamically added examples
    example_counter = 1
    while f'example_text_{example_counter}' in request.form:
        # Fetch values for each example
        example_text = request.form[f'example_text_{example_counter}']
        ex_translation = request.form[f'example_translation_{example_counter}']
        ex_transliteration = request.form[f'example_transliteration_{example_counter}']
        ex_glosses = request.form[f'glosses_{example_counter}']
        comment = request.form[f'comment_{example_counter}']

        # Create a unique URI for each example
        example_uri = cx[f"{construction_name_cleaned}_Ex_{chr(64 + example_counter)}"]

        # Add RDF triples for the example if needed
        if example_text.strip(): #TODO actually, there should not be any example without a text; but if users create an example by mistake, this needs to be handled
            example_text_no_annotation = re.sub(r'\[([^\]]*)\](\d+)', r'\1', example_text)
            g.add((cx[construction_name_cleaned], cx.hasExample, example_uri))
            g.add((example_uri, RDF.type, cx.Example))
            g.add((example_uri, cx.hasAnnotatedText, Literal(example_text)))
            g.add((example_uri, cx.hasText, Literal(example_text_no_annotation)))
        if ex_translation.strip():
            g.add((example_uri, cx.hasTranslation, Literal(ex_translation)))
        if ex_transliteration.strip():
            g.add((example_uri, cx.hasTransliteration, Literal(ex_transliteration)))
        if ex_glosses.strip():
            g.add((example_uri, cx.hasGlosses, Literal(ex_glosses)))
        if comment.strip():
            g.add((example_uri, RDFS.comment, Literal(comment)))

        example_counter += 1

###################################################
### IMPLEMENT RESEARCH DATA #TODO
###################################################

    # Add a comment about research data:
    if research_data.strip():
        g.add((cx[construction_name_cleaned], RDFS.comment, Literal(research_data)))

###################################################
### SERIALIZE THE RDF GRAPH TO A .ttl FILE
###################################################

    # Create a time stamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # The file is stored in "user_graphs" subfolder, ensure it exists
    os.makedirs(os.path.join(current_app.instance_path, "user_graphs"), exist_ok=True)

    # Create the file path within the subfolder
    file_path = os.path.join(
        current_app.instance_path,
        "user_graphs",
        f'{user_name.split("/")[-1]}_{timestamp}_cx.ttl'
    )

    # Serialize the ttl file
    g.serialize(destination=file_path, format='turtle')

    # The user downloads the file
    return send_file(file_path, as_attachment=True)
