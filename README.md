# Research Constructicon Web App

A Flask-based web application for submitting, managing and displaying linguistic constructions in a research constructicon.

## Table of Contents
1. [Definitions](#definitions)
2. [Folder Structure](#folder-structure)
3. [System Requirements](#system-requirements)
4. [Running the App](#running-the-app)
5. [Submission Process](#submission-process)
6. [Adding a New Language](#adding-a-new-language)
7. [Support](#support)
8. [Citation](#citation)

## Definitions
- **Users**: Visitors who browse the webpage and view construction entries.
- **Contributors**: Users who submit constructions to the constructicon.
- **Editor**: Responsible for proofreading submissions, ensuring correctness, and managing the addition of new languages and constructions.

## Folder Structure

```
.
├── Abox/                  # Stores A-box files (e.g., membr.ttl, cx.ttl, references.ttl)
├── app_entries/           # Flask app for construction entries
│   └── templates          # HTML for construction entries
├── app_form/              # Flask app for the submission form
│   └── templates          # HTML for the submission form
├── instances/
│   └── Submissions/       # Stores submitted .ttl files
│   └── user_graphs/       # RDF saved automatically upon submission; as backup
├── main_app/              # Flask app for the landing page
├── old_files/             # Legacy files
├── ontologies/            # RDF ontologies
├── static/
│   ├── css/               # Stylesheets
│   ├── data/
│   │   └── language_tree.json  # Language data
│   └── js/                # JavaScript files
├── templates/             # HTML templates
├── app.py                 # Main Flask application
├── create-Abox-after-new-submission.py  # Main Flask application
└── requirements.txt       # Python dependencies
```

## System Requirements
- **Python**: 3.14 or higher
- **Dependencies**: Listed in `requirements.txt`

## Running the App
Run the main Flask application:
```bash
python app.py
```
The app will start locally, typically at `http://127.0.0.1:5000/`.

## Submission Process
1. **Contributor**:
   - Fill out the online form to describe the construction.
   - Download the generated `.ttl` file.
   - Email the file to the editor, including any comments or notes.

2. **Editor**:
   - Save the `.ttl` file in `instances/Submissions/`. At this stage, the construction only appears in development mode.
   - Review the submission and communicate with the contributor if needed.
   - Once approved, run the `create-Abox-after-new-submission.py` script to update the A-box files (`membr.ttl`, `cx.ttl`, `references.ttl`) and add inferences. The construction will be displayed on the server.

## Adding a New Language
1. **Contributor**:
   - Notify the editor of the need to add a new language, preferably before submission.

2. **Editor**:
   - The editor checks the [ISO 639-3 standard](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Name_Index.tab).
   - If the language exists, use the ISO label and code. If not, identify the closest metalanguage/variety and create a new code (e.g., `engUsSpo` for "Spoken American English").
   - Add the language to:
     - `ontologies/lg.rdf`
     - `static/data/language_tree.json`
   - Always include both the metalanguage and variety.

## Support
For questions or support, contact the editor via email.

## Citation
Please cite as:

Winckel, Elodie. 2025. Defining relationships in the constructional network: A Semantic Web ontology for Construction Grammar. Lexicographica 41(1). 299–317. https://doi.org/10.1515/lex-2025-0012.
