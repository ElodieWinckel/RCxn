# Research Constructicon ontology: documentation

**Author**: Elodie Winckel

**Contributors**: Peter Uhrig, Stephanie Evert

\---

**Table of content**

[MODULE Constructicon (rcxn)](#module-constructicon-%28rcxn%29)

[Title](#title)

[Semantic function of the construction](#semantic-function-of-the-construction)

[Slots](#slots)

[Metadata](#metadata)

[Similar cxs in other Cxns](#similar-cxs-in-other-cxns)

[MODULE Casa (casa)](#module-casa-%28casa%29)

[MODULE Research (rsrch)](#module-research-%28rsrch%29)

[Research Question](#research-question)

[Findings](#findings)

[MODULE Language (lg)](#module-language-%28lg%29)

[MODULE Text](#module-text)

[MODULE Links](#module-links)

[MODULE Evidence (evid)](#module-evidence-%28evid%29)

[Colloprofiles](#colloprofiles)

[MODULE Comparative concepts (compcon)](#module-comparative-concepts-%28compcon%29)

[MODULE Gesture constructions (gest)](#module-gesture-constructions-%28gest%29)

[Description of gesture constructions](#description-of-gesture-constructions)

[Multimodal constructions (using gesture constructions)](#multimodal-constructions-%28using-gesture-constructions%29)

[NOTE on bibliographic references](#bibliographic-references)

# MODULE Constructicon (rcxn) {#module-constructicon-(rcxn)}

Prefix (rcxn): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rcxn#

This module uses RDF Schema (rdfs; label), Schema Datatype (xsd; date), Olia (olia; DiscourseFeature \& oliatop; SemanticRole) and the research module (rsrch; Project).

|Class rcxn#Construction||
|-|-|
|definition|Construction; linguistic sign with a form component and a meaning component. A network of constructions builds a Constructicon.|

## Title {#title}

|Property rcxn#hasTitle||
|-|-|
|definition|Property that relates a construction to its name.|
|domain (subject)|rcxn#Construction|
|range (object)|Literal|
|label|Title (en)|

## Semantic function of the construction {#semantic-function-of-the-construction}

|Class rcxn#ConstructionMeaning||
|-|-|
|definition|A construction has both form and meaning. ConstructionMeaning refers to the meaning of a construction.|

|Property rcxn#hasConstructionMeaning||
|-|-|
|definition|Property that relates a construction to its meaning component (an object of type ConstructionMeaning).|
|domain (subject)|rcxn#Construction|
|range (object)|rcxn#ConstructionMeaning|

|Property rcxn#hasMeaning||
|-|-|
|definition|Property that relates the meaning component of a construction to the corresponding plaintext description of this meaning.|
|domain (subject)|rcxn#ConstructionMeaning|
|range (object)|Literal|
|label|Meaning of the construction (en)|

|Property rcxn#usesImageSchema||
|-|-|
|definition|Relates the meaning component of a construction to the cognitive pattern that it is based on (i.e., containment or path) and that helps convey meaning through spatial or experiential metaphors.|
|domain (subject)|rcxn#ConstructionMeaning|
|range (object)|Literal|
|label|Image-Schema|

## Slots {#slots}

|Class rcxn#Slot||
|-|-|
|definition|Construction elements in the construction. They encompass both slot elements, which are positions where specific lexical items or phrases can be inserted, and lexically defined elements, which are fixed words or phrases that contribute to the construction's specific form and meaning. In constructicography, construction elements are linked together by "sequential" links.|

|Class rcxn#SlotObligatory||
|-|-|
|definition|Non-optional construction elements that need to be realized.|
|subclass of|rcxn#Slot|
|disjoint with|rcxn#SlotOptional|

|Class rcxn#SlotOptional||
|-|-|
|definition|Optional construction elements; the meaning of the construction is not dependent on its realization.|
|subclass of|rcxn#Slot|
|disjoint with|rcxn#SlotObligatory|

|Property rcxn#hasSlots||
|-|-|
|definition|Relates a construction to the sequence of construction elements that constitutes it.|
|domain (subject)|rcxn#Construction|
|range (object)|Sequence|

RDF proposes different types of groups:  
- bags: unordered  
- sequence: ordered  
- collection/list: ordered and exhaustive (no element can be added), based on a first/rest recursive structure.

We are using sequences because the elements should be presented in a fixed order on the website, even if the linearization is free in the construction. Linearization (word order) is considered separately.

|Class rcxn#SlotForm||
|-|-|
|definition|Formal features of a construction element.|

|Property rcxn#hasSlotForm||
|-|-|
|definition|Relates a construction element to its formal features.|
|domain (subject)|rcxn#Slot|
|range (object)|rcxn#SlotForm|
|label|Formal properties|

|Property rcxn#hasPhonology||
|-|-|
|definition|Phonological form of the construction element.|
|domain (subject)|rcxn#SlotForm|
|range (object)|Literal|
|label|Phonology|

|Property rcxn#hasRoot||
|-|-|
|definition|Describes the form of a construction element as based on a certain root.|
|domain (subject)|rcxn#SlotForm|
|range (object)|Literal|
|label|Root (en)|

|Property rcxn#hasStem||
|-|-|
|definition|Describes the form of a construction element as based on a certain stem or lemma.|
|domain (subject)|rcxn#SlotForm|
|range (object)|rcxn#Construction|
|label|Stem / Lemma (en)|

|Property rcxn#hasSurfaceForm||
|-|-|
|definition|Describes the form of a construction element as having a specific surface form.|
|domain (subject)|rcxn#SlotForm|
|range (object)|Literal|
|label|Surface form (en)|

|Property rcxn#hasSyntacticForm||
|-|-|
|definition|Identifies the form of the element with that of a construction: typically, it would be a morphosyntactic category (a type of morpheme, a part of speech, a phrase type, a clause type).|
|domain (subject)|rcxn#SlotForm|
|range (object)|rcxn#Construction|
|label|Syntactic form (en)|

|Property rcxn#hasSyntacticFunction||
|-|-|
|definition|Relates the construction element to its function. Typical functions are “subject”, “complement”, “modifier” etc.|
|domain (subject)|rcxn#Slot|
|range (object)|Literal|
|label|Syntactic function (en)|

|Property rcxn#hasSemanticContribution||
|-|-|
|definition|Describes the meaning (e.g., semantic role) of the construction element in the construction.|
|domain (subject)|rcxn#Slot|

|Property rcxn#hasSemanticRole||
|-|-|
|definition|Describes the semantic role of the construction element in the construction. The semantic roles are defined by the OLiA ontology.|
|subproperty of|rcxn#hasSemanticContribution|
|range (object)|oliatop:SemanticRole|
|label|Semantic role (en)|

|Property rcxn#hasOtherSemanticContribution||
|-|-|
|definition|Describes the meaning of the construction element in the construction that cannot be captured by the semantic roles of the OLiA ontology.|
|subproperty of|rcxn#hasSemanticContribution|
|range (object)|Literal|
|label|Semantic contribution (en)|

|Property rcxn#hasSemanticProperty||
|-|-|
|definition|Describes any loosely defined semantic category that the construction element (typically a word) should belong to. E.g. “the noun has a generic meaning” or “the verb denotes a destructive event”|
|domain (subject)|rcxn#Slot|
|range (object)|Literal|
|label|Semantic property (en)|

To describe information structure, the current ontology is very simple. The ontology OLiA provides a more detailed and accurate vocabulary, which we might want to adopt in the future.

|Class rcxn#informationStructure||
|-|-|
|definition||

|Class rcxn#Focus||
|-|-|
|definition|Focus indicates the presence of alternatives that are relevant for the interpretation of linguistic expressions. (Féry et al. 2007) That part of an expression which provides the most relevant information in a particular context as opposed to the (not so relevant) rest of information making up the background of the utterance. Typically, focus on a subexpression indicates that it is selected from possible alternatives that are either implicit or given explicitly, whereas the background can be derived from the context of the utterance. (SFB632 Guidelines) Foci are classified here according to their discourse function (independently from their structural realization).|
|is defined by|olia#Focus|
|equivalent to|olia#Focus|
|subclass of|rcxn#informationStructure|
|label|Focus|

|Class rcxn#Topic||
|-|-|
|definition|The topic constituent identifies the entity or set of entities under which the information expressed in the comment constituent should be stored in the CG content. The notion of topic is best understood as a kind of address or file card which specifies the individual or set about which the remainder of the sentence makes a comment (see Reinhart 1981 for such a concept of topicality). It has no truthconditional effect except that it presupposes the existence of that individual. In this sense, the complement of ‘topic’ is ‘comment,’ which can itself be partitioned into a focused and a backgrounded part. Sentences usually have only one topic, but can also have none, or more than one. Following Jacobs (2001), topics can be aboutness or frame-setting topics, and the means to express a topic in the grammar can be pinpointed rather precisely in terms of which syntactic and intonational preferences the topic displays, at least in an intonation language. However, according to Féry’s theses, none of these properties are definitional for topic. Rather they express preferences as to how a ‘good’ topic has to be realized (see also Jacobs 2001 for a similar view). (Féry et al. 2007)|
|is defined by|olia#Topic|
|equivalent to|olia#Topic|
|subclass of|rcxn#informationStructure|
|label|Topic|

|Class rcxn#Background||
|-|-|
|definition|The Background is in complementary distribution with the Focus. Typically, the background is discourse-given and can be derived from the context of the utterance. It is the not so relevant information of the utterance.|
|subclass of|rcxn#informationStructure|
|label|Background|

|Class rcxn#ISComment||
|-|-|
|definition|The Comment is in complementary distribution with the Topic. It is what is said about the topic, the main predication of the utterance.|
|subclass of|rcxn#informationStructure|
|label|Comment|

|Property rcxn#hasIS||
|-|-|
|definition|The construction element is part of the Focus or Background / Topic or Comment of the full utterance.|
|domain (subject)|rcxn#Slot|
|range (object)|rcxn#informationStructure|
|label|Information Structure|

## Metadata {#metadata}

|Class rcxn#Metadata||
|-|-|
|definition|Non-linguistic information on the construction entry, such as the persons involved in the creation of the entry or the sources.|

|Property rcxn#hasMetadata||
|-|-|
|definition|Relates a construction to the non-linguistic information about its entry (its metadata).|
|domain (subject)|rcxn#Construction|
|range (object)|rcxn#Metadata|

|Property rcxn#annotator||
|-|-|
|definition|Relates a construction entry’s metadata to the person who created it.|
|domain (subject)|rcxn#Metadata|
|range (object)|rsrch#Member|
|label|Annotator (en)|

Note that we use dcterm:created in the database to store the date of creation of the construction entry.

## Similar cxs in other Cxns {#similar-cxs-in-other-cxns}

To date, links to URLs of other reference constructicons are stored via the property RDFS:seeAlso. We might, however, change this is the future.

# MODULE Casa (casa) {#module-casa-(casa)}

Prefix (casa): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/casa#

Because the Research Constructicon project is tightly linked to the CASA Project ([https://constructicon.de/](https://constructicon.de/)), and because the entries of CASA are imported in the Research Constructicon, we needed to adopt some of their terminology.

|Property casa#hasCasaSyntacticFunction||
|-|-|
|definition|Relates the construction element to its function, using CASA’s methodology. Typical functions are “potential subject”, “Obj” (object), “Attr” (attribute) etc.|
|domain (subject)|rcxn#Slot|
|range (object)|Literal|
|label|Syntactic function (CASA terminology) (en)|

# MODULE Research (rsrch) {#module-research-(rsrch)}

Prefix (rsrch): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/rsrch#

This module uses RDF Schema (rdfs; label) and Friend-of-a-friend (foaf; Person, Project).

|Class rsrch#Member||
|-|-|
|definition|Member of the research group and/or contributors to the Constructicon.|
|subclass of|foaf:Person|

|Class rsrch#Researcher||
|-|-|
|definition|PhD student researcher working in the research group.|
|subclass of|rcxn#Member|
|disjoint with|PI, PostDoc|

|Class rsrch#PostDoc||
|-|-|
|definition|Post-doctoral researcher working in the research group.|
|subclass of|rcxn#Member|
|disjoint with|Researcher|

|Class rsrch#PI||
|-|-|
|definition|Researchers supervising or otherwise involved in a research project.|
|subclass of|rcxn#Member|
|disjoint with|Researcher|

## Research Question {#research-question}

|Class rsrch#Project||
|-|-|
|definition|A research question, i.e., a concise inquiry that defines the academic focus of a researcher. Within the terminology of the Research Training Group, the main research question of a PhD candidate for their thesis is called a “project”.|
|subclass of|foaf:Project|

|Property rsrch#hasResearchQuestion||
|-|-|
|definition|Property that breaks down a project or research question and relates it to smaller research questions.|
|domain (subject)|rsrch#Project|
|range (object)|rsrch#Project|
|Characteristics|Transitive, Asymmetric|

|Property rsrch#projectName||
|-|-|
|definition|Property that relates the URI of a project to its exact label.|
|domain (subject)|rsrch#Project|
|range (object)|Literal|

## Findings {#findings}

Research questions lead to findings. Findings are based on research data on the one hand and constructions on the other hand.

|Class rsrch#Finding||
|-|-|
|definition|Research on a research question leads to one or several finding(s). They are statements, answers to the research question.|

|Property rsrch#hasFindings||
|-|-|
|definition|Property that links a research question to the finding(s) answering this research question.|
|domain (subject)|rsrch#Project|
|range (object)|rsrch#Finding|
|Characteristics|Asymmetric|

|Property rsrch#basedOn||
|-|-|
|definition|Property that relates a finding to the evidence for the finding: either research data or construction(s).|
|domain (subject)|rsrch#Finding|
|range (object)|cx#Construction|
|Characteristics|Asymmetric|

# MODULE Language (lg) {#module-language-(lg)}

Prefix (lg): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#

We make here a distinction between “Macrolanguages” and “Language Variety”.

Macrolanguages are defined by the norm ISO 639-3 ([https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3\_Name\_Index.tab](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Name_Index.tab)). Some of the languages defined by the norm ISO 639-3 are mapped to a macrolanguage ([https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3-macrolanguages.tab](https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3-macrolanguages.tab)), in which case there are considered a language variety in our terminology. For example, “Literary Chinese” (code lzh) is a variety of “Chinese” (code zho). Languages defined by the norm ISO 639-3 that have no Macro-languages are considered in our terminology as being a macrolanguage.

Contributors of the RCxn can create language varieties as fine grained as they wish, but need to range them under a language defined by the norm ISO 639-3. By doing so, they can specify any of the following:  
- (macro-)language  
- time  
- dialect area  
- modality (written/spoken)  
- genre (e.g., legal, informal, etc.)

|Class lg#lg||
|-|-|
|label|Language|
|definition|Language constructional space that the construction is a part of.|

|Class lg#macrolanguage||
|-|-|
|label|Macrolanguage|
|defined by|ISO 639-3|
|subclass of|lg:lg|

|Class lg#variety||
|-|-|
|label|Language Variety|
|definition|Language constructional space that the construction is a part of. It contains indications about the language name, but also register, modality, dialectal area and temporality when relevant for the description of the construction.|
|subclass of|lg:lg|

|Property lg#isVarietyOf||
|-|-|
|definition|Property that relates a more specific language variety to a more generic language (language variety or macrolanguage).|
|domain (subject)|lg#variety|
|range (object)|lg#lg|

|Property lg#partOfLanguage||
|-|-|
|definition|Property that relates a construction to its language.|
|domain (subject)|rcxn#Construction|
|range (object)|lg#lg|

Our hierarchy of languages is implemented as individuals directly in the ontology. The IRI is the ISO code when available. For example, German is lg#deu:

|<!-- https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#deu -->     <owl:NamedIndividual rdf:about="https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#deu">         <rdf:type rdf:resource="https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/lg#macrolanguage"/>         <rdfs:label xml:lang="en">German</rdfs:label>     </owl:NamedIndividual>|
|-|

# MODULE Text {#module-text}

This ontology is work in progress. It should deal with translation, transliteration, transcription, and glosses. Possibly, we could also add a property that links an example to the source of the example.

# MODULE Links {#module-links}

The ontology for links is presented in the following publication:  
Winckel, Elodie. 2025. Defining relationships in the constructional network: A Semantic Web ontology for Construction Grammar. *Lexicographica* 41(1). 299–317. [https://doi.org/10.1515/lex-2025-0012](https://doi.org/10.1515/lex-2025-0012).

Since this first version 1.0, I added the following properties (which are therefore part of the 1.1 version):

|Property links#isMetaphoricalExtensionOf||
|-|-|
|definition|Links back the metaphorical extension to the construction with literal meaning (see metaphorical link).|
|subproperty of|links#LanguageInternalLink|
|label|is a metaphorical extension of|

As a corollary to hasSyntacticForm, it was necessary to add the link #elementOf that relates a construction back to all constructions that use it (for example, the NP construction will potentially be used by many constructions).

|Property links#elementOf||
|-|-|
|definition|Relates a construction to the constructions that it is a part of. If element A uses B, then B is an element of A.|
|subproperty of|links#LanguageInternalLink|
|label|Element of (en)|

# MODULE Evidence (evid) {#module-evidence-(evid)}

Prefix (evid): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/evid#

Work-in-progress: the module should comprise definition of resources to deal with colloprofiles, refer to repositories with data and/or analyses.

This ontology also includes a way to link to bibliographical references. This part will be based on Dublin Core (db).

## Colloprofiles {#colloprofiles}

Note that our proposal for colloprofiles has many similarities with collocations in the the *module for frequency, attestation and corpus information* (frac) of the OntoLex Lexicon Model for Ontologies ([https://github.com/ontolex/frequency-attestation-corpus-information](https://github.com/ontolex/frequency-attestation-corpus-information)). The frac module, and especially the way collocations are implemented, is however only a draft version and might still change. It is also unclear if colloprofiles completely fit into it. We are therefore relying on our own ontology module for now. But the following properties are in a provisory stage, as we might switch the design to align with ontolex in the future.

|Property evid#colloprofile||
|-|-|
|definition|Describes the colloprofile of a construction element. If the construction element is a slot that can be filled by various formal realizations, the colloprofile enumerates the (most frequent) realizations along with their respective frequencies.|
|domain (subject)|rcxn#Slot|
|range (object)|rdf:Bag|
|label|Colloprofile (en)|

|Property evid#filler||
|-|-|
|definition|A potential filler (i.e., formal realization) of a slot. A bag of fillers builds the colloprofile of the slot.|
|range (object)|Literal|
|label|Filler (en)|

The frequency is implemented with frac:frequency

Example code snippet:

|cx:eng\_ThisclosetoVingconstruction\_3 a rcxn:SlotOptional ;     evid:colloprofile (         \[ evid:filler "be"; frac:frequency \[ a cx:CorpusX ; rdf:value "327"^^xsd:int]]         \[ evid:filler "come"; frac:frequency \[ a cx:CorpusX ; rdf:value "109"^^xsd:int]]         \[ evid:filler "get"; frac:frequency \[ a cx:CorpusX ; rdf:value "11"^^xsd:int]] ) ;     rcxn:hasSlotForm cx:eng\_ThisclosetoVingconstruction\_3\_Form .|
|-|

## Bibliographic references {#bibliographic-references}

We encourage contributors to provide bibliographic references to a construction entry. For this, we create **bibliographic entries**, collect them in a **bibliography**, and attach this bibliography to the metadata of the construction.

**Bibliographic entries**: The URI of the bibliographic entry uses the prefix references: ([https://bdlweb.phil.uni-erlangen.de/RCxn/Abox/references#](https://bdlweb.phil.uni-erlangen.de/RCxn/Abox/references#)).

|Property evid#biblio||
|-|-|
|definition|The bibliographic entry that informed the construction entry.|
|range (object)|Literal|
|label|Bibliographic entry (en)|

**Bibliography**: The bibliography is defined as a dcterms:Collection. It is linked to each bibliographic entry via the predicate dcterms:hasPart. The URI of the bibliography is typically the URI of the construction followed by \_Sources.

**Metadata**: To link the (metadata of the) construction to its bibliography, we use the predicate dcterms:references.

Example code snippet:

|cx:arzCai\_Ditransitiveconstruction\_Sources a dcmitype:Collection ;     dcterm:hasPart references:3123c19c-3f37-43ae-9471-d753fdd7839c,         references:c3138c0e-1108-404a-96a8-0ade960b6ca4 . references:3123c19c-3f37-43ae-9471-d753fdd7839c evid:biblio "Woidich, Manfred. 2006. Das Kairensisch-Arabische. Eine Grammatik. Wiesbaden: Harrassowitz." . references:c3138c0e-1108-404a-96a8-0ade960b6ca4 evid:biblio "Diem, Werner. 2002. Translokative Verben im Arabischen. Wiesbaden: Harrassowitz." .|
|-|

## Studies

|Class evid#Study||
|-|-|
|label|Study|
|definition|An empirical study to investigate a linguistic phenomenon. It addresses a specific research question (or set of closely related questions) under a specific methodology.|

|Class evid#BehavioralExperiment||
|-|-|
|label|Behavioral experiment|
|definition|An empirical study in linguistics that uses controlled, systematic tasks to investigate linguistic behavior in human participants.|
|subclass of|evid#Study|

|Property evid#relevantFor||
|-|-|
|definition|Establishes a connection between the linguistic study and the construction or phenomenon it aims to explore.|
|domain (subject)|evid#Study|
|range (object)|rcxn#Construction|
|inverse of|evid#basedOnStudy|
|label|Relevant construction (en)|

|Property evid#basedOnStudy||
|-|-|
|definition|Establishes a connection between a construction and a linguistic study whose results informed the construction’s description.|
|domain (subject)|rcxn#Construction|
|range (object)|evid#Study|
|inverse of|evid#relevantFor|
|label|based on (en)|

|Property evid#publishedIn||
|-|-|
|definition|Relates a linguistic study to the bibliographic entry that reports it.|
|domain (subject)|evid#Study|
|range (object)|Literal|
|label|Publication (en)|

|Property evid#repository||
|-|-|
|definition|Relates a linguistic study to the online repository which contains research data, material and/or other research resources.|
|domain (subject)|evid#Study|
|range (object)|Literal|
|label|Repository (en)|

|Property evid#summary||
|-|-|
|definition|Describes the content (method, results) of a linguistic study.|
|domain (subject)|evid#Study|
|range (object)|Literal|
|label|Summary (en)|

# MODULE Comparative concepts (compcon) {#module-comparative-concepts-(compcon)}

Prefix (compcon): https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/compcon#

The ontology exists, but was not really defined by us. Description is work-in-progress.

# MODULE Gesture constructions (gest) {#module-gesture-constructions-(gest)}

Prefix (gest): [https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/gest#](https://bdlweb.phil.uni-erlangen.de/RCxn/ontologies/gest#)

This module uses #Construction and #Slot from the rcxn module.

## Description of gesture constructions {#description-of-gesture-constructions}

|Class gest#GestureConstruction||
|-|-|
|definition|A specific bodily gesture paired with a particular semantic or pragmatic function within a linguistic context.|
|subclass of|rcxn#Construction|
|label|Gesture construction (en)|

The formal properties gest#handedness, gest#handshape, gest#movement, gest#orientation, gest#position and gest#timing can all refer to either the form of the whole construction (gest#GestureForm) or its phases (gest#Phase). For this reason, an encompassing class gest#GestureFormalComponent was needed.

|Class gest#GestureFormalComponent||
|-|-|
|definition|A class that subsumes both the overall form of a gestural construction and its individual temporal phases.|
|label|Gesture formal component (en)|

|Class gest#GestureForm||
|-|-|
|definition|The description of the full manifestation of a gesture (rather than its phases).|
|subclass of|gest#GestureFormalComponent|
|label|Form of the gesture (en)|

|Class gest#Phase||
|-|-|
|definition|The formal description of a temporally distinct segment within the unfolding of a gestural construction.|
|subclass of|gest#GestureFormalComponent|
|label|Phase (en)|

The construction itself is linked to gest#GestureForm for its formal component. However, gest#GestureForm can be a sequence of phases.

|Property gest#hasForm||
|-|-|
|definition|Relates a gesture construction to its formal description.|
|domain (subject)|gest#GestureConstruction|
|range (object)|gest#GestureForm|
|label|has form|

|Class gest#Handedness||
|-|-|
|label|Handedness (en)|

|Class gest#OneHand||
|-|-|
|definition|A gesture construction performed predominantly using one hand, with the other hand either inactive or minimally involved.|
|subclass of|gest#Handedness|
|label|One-Handed (en)|

|Class gest#LeftHand||
|-|-|
|definition|A gesture construction performed predominantly using the left hand, with the right hand either inactive or minimally involved.|
|subclass of|gest#OneHand|
|label|Left-Handed (en)|

|Class gest#RightHand||
|-|-|
|definition|A gesture construction performed predominantly using the right hand, with the right hand either inactive or minimally involved.|
|subclass of|gest#OneHand|
|label|Right-Handed (en)|

|Class gest#TwoHands||
|-|-|
|definition|A gesture construction performed using both hands simultaneously.|
|subclass of|gest#Handedness|
|label|Two-Handed (en)|

|Property gest#handedness||
|-|-|
|definition|Refers to the hand or hands used in the execution of a gesture construction.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|gest#Handedness|
|label|Handedness|

|Property gest#handshape||
|-|-|
|definition|Refers to the configuration of the hand(s) during the execution of a gesture construction, specifying the physical arrangement of fingers and thumb.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|Literal|
|label|Handshape|

|Property gest#movement||
|-|-|
|definition|Refers to the dynamic trajectory, direction, and manner of motion involved in a gesture construction.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|Literal|
|label|Movement|

|Property gest#orientation||
|-|-|
|definition|Refers to the direction in which the hand(s) are facing during a gesture construction, specifying the spatial alignment of the palm, fingers, or hand surface.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|Literal|
|label|Orientation|

|Property gest#position||
|-|-|
|definition|Refers to the spatial location of the hand(s) relative to the body during a gesture construction.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|Literal|
|label|Position|

|Property gest#timing||
|-|-|
|definition|Refers to the temporal characteristics of a gesture construction, such as duration, ryththm or stroke.|
|domain (subject)|gest#GestureFormalComponent|
|range (object)|Literal|
|label|Timing|

|Class gest#GestureMeaning||
|-|-|
|definition|The description of the functional and interpretive significance of a gesture construction.|
|subclass of|gest#Handedness|
|label|Meaning of the gesture|

|Property gest#hasMeaning||
|-|-|
|definition|Relates a gesture construction to the description of its meaning and/or function.|
|domain (subject)|gest#GestureConstruction|
|range (object)|gest#GestureMeaning|
|label|has meaning|

|Property gest#semanticProperty||
|-|-|
|definition|Specifies the conceptual or referential content of the gesture construction.|
|domain (subject)|gest#GestureMeaning|
|range (object)|Literal|
|label|Semantic property|

|Property gest#pragmaticProperty||
|-|-|
|definition|Specifies the functional role in discourse of a gesture construction.|
|domain (subject)|gest#GestureMeaning|
|range (object)|Literal|
|label|Pragmatic property|

|Property gest#discourseFunctionalProperty||
|-|-|
|definition|Describes the role a gesture construction plays in discourse.|
|domain (subject)|gest#GestureMeaning|
|range (object)|Literal|
|label|Discourse-functional property|

## Multimodal constructions (using gesture constructions) {#multimodal-constructions-(using-gesture-constructions)}

Notice that the multimodal construction is not linked directly to a gesture construction, but to its usage of a gesture construction (which can in turn be linked to the gesture construction in question). This allows us to describe the usage further with features specific to the multimodal construction that do not describe the gesture construction (specifically: when the usage starts and ends).

|Class gest#GestureUsage||
|-|-|
|definition|Denotes the non-verbal, gestural components associated with a linguistic construction.|
|label|Gesture usage of the construction (en)|

|Property gest#hasGesture||
|-|-|
|definition|Relates a multimodal construction to its usage of a gesture construction.|
|domain (subject)|rcxn#Construction|
|range (object)|gest#GestureUsage|
|label|has gesture|

|Property gest#uses||
|-|-|
|definition|Relates the IRI for the gesture usage of the construction to the gesture construction(s) that are in use.|
|domain (subject)|gest#GestureUsage|
|range (object)|gest#GestureConstruction|
|label|uses the gesture construction|

|Property gest#starts||
|-|-|
|definition|Describes the usage of a gesture construction with the specific verbal construction element whose realization coincides with the onset of the gesture.|
|domain (subject)|gest#GestureUsage|
|range (object)|rcxn#Slot|
|label|starts with|

|Property gest#ends||
|-|-|
|definition|Describes the usage of a gesture construction with the specific verbal construction element whose realization coincides with the end of the gesture.|
|domain (subject)|gest#GestureUsage|
|range (object)|rcxn#Slot|
|label|ends with|



