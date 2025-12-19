// Generates the fields for constructions elements
function generateFields() {
    const elementNb = document.getElementById('element_nb').value;
    const container = document.getElementById('ElementsContainer');
    const infoContainer = document.getElementById('infoStructureContainer');
    container.innerHTML = '';
    infoContainer.innerHTML = '';
    const constructionName = document.getElementById('construction').value.replace(/\s+/g, '');
    for (let i = 0; i < elementNb; i++) {
        // Create a clickable header for each element
        const elementHeader = document.createElement('h3');
        elementHeader.textContent = `Element ${i + 1} `;
        const toggleIcon = document.createElement('span');
        toggleIcon.textContent = '+ ';
        toggleIcon.id = `toggleIcon_${i + 1}`;
        elementHeader.prepend(toggleIcon);
        elementHeader.style.cursor = 'pointer';
        elementHeader.onclick = function() { toggleElement(i + 1); };

        // Create a div to hold the details (hidden by default)
        const elementDetails = document.createElement('div');
        elementDetails.id = `elementDetails_${i + 1}`;
        elementDetails.style.display = 'none';

        // Create the dropdown multiple-choice field for optionality
        const optionalityLabel = document.createElement('label');
        optionalityLabel.textContent = 'Optionality of the element:';
        const optionalitySelect = document.createElement('select');
        optionalitySelect.name = `optionality_${i + 1}`;
        optionalitySelect.required = true;

        const nonOptionalOption = document.createElement('option');
        nonOptionalOption.value = 'non-optional';
        nonOptionalOption.textContent = 'Non-optional element';
        nonOptionalOption.selected = true;

        const optionalOption = document.createElement('option');
        optionalOption.value = 'optional';
        optionalOption.textContent = 'Optional element';

        optionalitySelect.appendChild(nonOptionalOption);
        optionalitySelect.appendChild(optionalOption);

        elementDetails.appendChild(optionalityLabel);
        elementDetails.appendChild(optionalitySelect);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for word order
        const orderLabel = document.createElement('label');
        orderLabel.textContent = `Word order specifications (recommended):`;
        // Create an info icon
        const orderInfoIcon = document.createElement('span');
        orderInfoIcon.className = 'info-icon';
        orderInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const orderTooltipText = document.createElement('span');
        orderTooltipText.className = 'tooltiptext';
        orderTooltipText.innerHTML = `
            By default, the order is considered to be irrelevant. Therefore, specifications should be spelled out.<br>
            For example: <br>
            Element 1 immediately before element 2.`;
        // Create a container for the label and the info icon
        const orderLabelContainer = document.createElement('div');
        orderLabelContainer.className = 'label-container';
        orderLabelContainer.appendChild(orderLabel);
        orderLabelContainer.appendChild(orderInfoIcon);
        const orderInput = document.createElement('input');
        orderInput.type = 'text';
        orderInput.name = `WordOrder_${i + 1}`;
        // Create a container for the input and the tooltip
        const orderTooltipContainer = document.createElement('div');
        orderTooltipContainer.className = 'tooltip-container';
        orderTooltipContainer.appendChild(orderInput);
        orderTooltipContainer.appendChild(orderTooltipText);
        // Add tooltip functionality to the info icon
        orderInfoIcon.appendChild(orderTooltipText);
        elementDetails.appendChild(orderLabelContainer);
        elementDetails.appendChild(orderTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for phonology
        const phonLabel = document.createElement('label');
        phonLabel.textContent = `Phonological form (optional):`;
        // Create an info icon
        const phonInfoIcon = document.createElement('span');
        phonInfoIcon.className = 'info-icon';
        phonInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const phonTooltipText = document.createElement('span');
        phonTooltipText.className = 'tooltiptext';
        phonTooltipText.innerHTML = `
            Use IPA alphabet (for example, copy-paste from the website ipa.typeit.org).`;
        // Create a container for the label and the info icon
        const phonLabelContainer = document.createElement('div');
        phonLabelContainer.className = 'label-container';
        phonLabelContainer.appendChild(phonLabel);
        phonLabelContainer.appendChild(phonInfoIcon);
        const phonInput = document.createElement('input');
        phonInput.type = 'text';
        phonInput.name = `phonology_${i + 1}`;
        // Create a container for the input and the tooltip
        const phonTooltipContainer = document.createElement('div');
        phonTooltipContainer.className = 'tooltip-container';
        phonTooltipContainer.appendChild(phonInput);
        phonTooltipContainer.appendChild(phonTooltipText);
        // Add tooltip functionality to the info icon
        phonInfoIcon.appendChild(phonTooltipText);
        elementDetails.appendChild(phonLabelContainer);
        elementDetails.appendChild(phonTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for surface form
        const surfaceLabel = document.createElement('label');
        surfaceLabel.textContent = `Surface form (optional):`;
        // Create an info icon
        const surfaceInfoIcon = document.createElement('span');
        surfaceInfoIcon.className = 'info-icon';
        surfaceInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const surfaceTooltipText = document.createElement('span');
        surfaceTooltipText.className = 'tooltiptext';
        surfaceTooltipText.innerHTML = `
            Use this when the element is a specific lexical item in a specific form. For lemmata, see another field below.<br>
            For example:<br>
            devil<br>
            what`;
        // Create a container for the label and the info icon
        const surfaceLabelContainer = document.createElement('div');
        surfaceLabelContainer.className = 'label-container';
        surfaceLabelContainer.appendChild(surfaceLabel);
        surfaceLabelContainer.appendChild(surfaceInfoIcon);
        const surfaceInput = document.createElement('input');
        surfaceInput.type = 'text';
        surfaceInput.name = `surface_form_${i + 1}`;
        // Create a container for the input and the tooltip
        const surfaceTooltipContainer = document.createElement('div');
        surfaceTooltipContainer.className = 'tooltip-container';
        surfaceTooltipContainer.appendChild(surfaceInput);
        surfaceTooltipContainer.appendChild(surfaceTooltipText);
        // Add tooltip functionality to the info icon
        surfaceInfoIcon.appendChild(surfaceTooltipText);
        elementDetails.appendChild(surfaceLabelContainer);
        elementDetails.appendChild(surfaceTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for root
        const rootLabel = document.createElement('label');
        rootLabel.textContent = `Root (optional):`;
        // Create an info icon
        const rootInfoIcon = document.createElement('span');
        rootInfoIcon.className = 'info-icon';
        rootInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const rootTooltipText = document.createElement('span');
        rootTooltipText.className = 'tooltiptext';
        rootTooltipText.innerHTML = `
            NB: You probably don't need this field if you entered a surface form above.<br>
            For example: <br>
            Latin: In "amare" (to love), "am-" is the root.`;
        // Create a container for the label and the info icon
        const rootLabelContainer = document.createElement('div');
        rootLabelContainer.className = 'label-container';
        rootLabelContainer.appendChild(rootLabel);
        rootLabelContainer.appendChild(rootInfoIcon);
        const rootInput = document.createElement('input');
        rootInput.type = 'text';
        rootInput.name = `root_${i + 1}`;
        // Create a container for the input and the tooltip
        const rootTooltipContainer = document.createElement('div');
        rootTooltipContainer.className = 'tooltip-container';
        rootTooltipContainer.appendChild(rootInput);
        rootTooltipContainer.appendChild(rootTooltipText);
        // Add tooltip functionality to the info icon
        rootInfoIcon.appendChild(rootTooltipText);
        elementDetails.appendChild(rootLabelContainer);
        elementDetails.appendChild(rootTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for stem
        const stemLabel = document.createElement('label');
        stemLabel.textContent = `Stem / Lemma (optional):`;
        // Create an info icon
        const stemInfoIcon = document.createElement('span');
        stemInfoIcon.className = 'info-icon';
        stemInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const stemTooltipText = document.createElement('span');
        stemTooltipText.className = 'tooltiptext';
        stemTooltipText.innerHTML = `
            NB: You probably don't need this field if you entered a surface form above.<br>
            For example: <br>
            English: talk (lemma) <br>
            Spanish: habl- (stem)`;
        // Create a container for the label and the info icon
        const stemLabelContainer = document.createElement('div');
        stemLabelContainer.className = 'label-container';
        stemLabelContainer.appendChild(stemLabel);
        stemLabelContainer.appendChild(stemInfoIcon);
        const stemInput = document.createElement('input');
        stemInput.type = 'text';
        stemInput.name = `stem_${i + 1}`;
        // Create a container for the input and the tooltip
        const stemTooltipContainer = document.createElement('div');
        stemTooltipContainer.className = 'tooltip-container';
        stemTooltipContainer.appendChild(stemInput);
        stemTooltipContainer.appendChild(stemTooltipText);
        // Add tooltip functionality to the info icon
        stemInfoIcon.appendChild(stemTooltipText);
        elementDetails.appendChild(stemLabelContainer);
        elementDetails.appendChild(stemTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for transliteration
        const transliterationLabel = document.createElement('label');
        transliterationLabel.textContent = `Transliteration (optional):`;
        const transliterationInput = document.createElement('input');
        transliterationInput.type = 'text';
        transliterationInput.name = `transliteration_${i + 1}`;
        elementDetails.appendChild(transliterationLabel);
        elementDetails.appendChild(transliterationInput);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for translation
        const translationLabel = document.createElement('label');
        translationLabel.textContent = `Translation (recommended):`;
        const translationInput = document.createElement('input');
        translationInput.type = 'text';
        translationInput.name = `translation_${i + 1}`;
        elementDetails.appendChild(translationLabel);
        elementDetails.appendChild(translationInput);
        elementDetails.appendChild(document.createElement('br'));

        // --- Syntactic Form field with autocomplete + multiple values ---
        const syntacticFormLabel = document.createElement('label');
        syntacticFormLabel.textContent = `Syntactic form(s) of element ${i + 1} (optional):`;

        // Input + button
        const syntacticFormInput = document.createElement('input');
        syntacticFormInput.type = 'text';
        syntacticFormInput.id = `syntactic_form_${i + 1}`;
        syntacticFormInput.placeholder = "Type construction name";

        // Autocomplete
        $(() => {
            $(`#syntactic_form_${i + 1}`).autocomplete({
                source: existingConstructions
            });
        });

        const addSyntacticFormBtn = document.createElement('button');
        addSyntacticFormBtn.type = 'button';
        addSyntacticFormBtn.textContent = 'Add';

        // Container for selected syntactic forms
        const selectedSyntacticFormDiv = document.createElement('div');
        selectedSyntacticFormDiv.id = `selected_syntactic_form_${i + 1}`;

        // Hidden input to store JSON list
        const hiddenSyntacticFormInput = document.createElement('input');
        hiddenSyntacticFormInput.type = 'hidden';
        hiddenSyntacticFormInput.id = `morphosyntactic_form_${i + 1}`;
        hiddenSyntacticFormInput.name = `morphosyntactic_form_${i + 1}`;

        // Logic to add and remove items
        let selectedSyntacticForms = [];

        addSyntacticFormBtn.onclick = function() {
            let value = syntacticFormInput.value.trim();
            if (value && !selectedSyntacticForms.includes(value)) {
                selectedSyntacticForms.push(value);
                updateSelectedSyntacticForms();
            }
            syntacticFormInput.value = '';
        };

        function updateSelectedSyntacticForms() {
            selectedSyntacticFormDiv.innerHTML = '';
            selectedSyntacticForms.forEach((form, index) => {
                let btn = document.createElement('button');
                btn.type = 'button';
                btn.textContent = form;
                btn.onclick = function() {
                    selectedSyntacticForms.splice(index, 1);
                    updateSelectedSyntacticForms();
                };
                selectedSyntacticFormDiv.appendChild(btn);
            });
            hiddenSyntacticFormInput.value = selectedSyntacticForms.length ? JSON.stringify(selectedSyntacticForms) : '[]';
        }

        // Append all
        elementDetails.appendChild(syntacticFormLabel);
        elementDetails.appendChild(syntacticFormInput);
        elementDetails.appendChild(addSyntacticFormBtn);
        elementDetails.appendChild(selectedSyntacticFormDiv);
        elementDetails.appendChild(hiddenSyntacticFormInput);
        elementDetails.appendChild(document.createElement('br'));


        // Create fields for syntactic function
        const syntacticFunctionLabel = document.createElement('label');
        syntacticFunctionLabel.textContent = `Syntactic function (optional):`;
        const syntacticFunctionInput = document.createElement('input');
        syntacticFunctionInput.type = 'text';
        syntacticFunctionInput.name = `syntactic_function_${i + 1}`;
        elementDetails.appendChild(syntacticFunctionLabel);
        elementDetails.appendChild(syntacticFunctionInput);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for semantic contribution
        const semanticContributionLabel = document.createElement('label');
        semanticContributionLabel.textContent = `Semantic contribution of the element (recommended):`;
        // Create dropdown (select element) for semantic contribution
        const semanticContributionSelect = document.createElement('select');
        semanticContributionSelect.name = `semantic_contribution_${i + 1}`;
        // Populate the dropdown with options from the 'semanticRoles' array
        semanticRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role;
            option.textContent = role;
            semanticContributionSelect.appendChild(option);
        });
        // Add "Other" option to the dropdown
        const semanticContributionOtherOption = document.createElement('option');
        semanticContributionOtherOption.value = 'Other';
        semanticContributionOtherOption.textContent = 'Other';
        semanticContributionSelect.appendChild(semanticContributionOtherOption);
        // Append the label and dropdown to the container
        elementDetails.appendChild(semanticContributionLabel);
        elementDetails.appendChild(semanticContributionSelect);
        elementDetails.appendChild(document.createElement('br'));
        // Create an input field for "Other" option (initially hidden)
        const semanticContributionOtherInput = document.createElement('input');
        semanticContributionOtherInput.type = 'text';
        semanticContributionOtherInput.name = `add_semantic_contribution_${i + 1}`;
        semanticContributionOtherInput.placeholder = 'Please specify';  // Placeholder text inside the input field
        semanticContributionOtherInput.style.display = 'none';  // Hidden by default
        // Append the "Other" input field to the container
        elementDetails.appendChild(semanticContributionOtherInput);
        // Event listener for showing/hiding the "Other" input field based on selection
        semanticContributionSelect.addEventListener('change', function() {
            if (semanticContributionSelect.value === 'Other') {
                semanticContributionOtherInput.style.display = 'inline';  // Show the input field
            } else {
                semanticContributionOtherInput.style.display = 'none';  // Hide the input field
            }
        });

        // Create fields for colloprofile
        const colloprofileLabel = document.createElement('label');
        colloprofileLabel.textContent = `Colloprofile (Provisional: enter different lexical items separated by semicolons, and indications about frequency in parentheses) (optional):`;
        const colloprofileInput = document.createElement('input');
        colloprofileInput.type = 'text';
        colloprofileInput.name = `colloprofile_${i + 1}`;
        elementDetails.appendChild(colloprofileLabel);
        elementDetails.appendChild(colloprofileInput);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for animacy (dropdown + optional free-text input)
        const animacyLabel = document.createElement('label');
        animacyLabel.textContent = `Animacy (optional):`;
        elementDetails.appendChild(animacyLabel);
        const animacySelect = document.createElement('select');
        animacySelect.name = `animacy_${i + 1}`;
        animacySelect.onchange = function() { toggleAnimacyInput(animacySelect, i + 1); };  // Change handler for "other" selection
        // First option: empty
        const animacyEmptyOption = document.createElement('option');
        animacyEmptyOption.value = '';
        animacyEmptyOption.textContent = '';
        // Second option: animate
        const animateOption = document.createElement('option');
        animateOption.value = 'Animate';
        animateOption.textContent = 'Animate';
        // Third option: inanimate
        const inanimateOption = document.createElement('option');
        inanimateOption.value = 'Inanimate';
        inanimateOption.textContent = 'Inanimate';
        // Option other
        const animacyOtherOption = document.createElement('option');
        animacyOtherOption.value = 'other';
        animacyOtherOption.textContent = 'Other';
        // Select option
        animacySelect.appendChild(animacyEmptyOption);
        animacySelect.appendChild(animateOption);
        animacySelect.appendChild(inanimateOption);
        animacySelect.appendChild(animacyOtherOption);
        elementDetails.appendChild(animacySelect);
        // Hidden input for "other" animacy (free-text input field)
        const otherAnimacyInput = document.createElement('input');
        otherAnimacyInput.type = 'text';
        otherAnimacyInput.name = `other_animacy_${i + 1}`;
        otherAnimacyInput.placeholder = 'Please specify';
        otherAnimacyInput.style.display = 'none'; // Hidden by default
        elementDetails.appendChild(otherAnimacyInput);
        elementDetails.appendChild(document.createElement('br'));
        // Function to toggle free-text input visibility for "other" animacy selection
        function toggleAnimacyInput(selectElement, elementIndex) {
            const otherAnimacyInput = document.getElementsByName(`other_animacy_${elementIndex}`)[0];
            if (selectElement.value === 'other') {
                otherAnimacyInput.style.display = 'block'; // Show input field when "other" is selected
            } else {
                otherAnimacyInput.style.display = 'none'; // Hide input field for other selections
            }
        }

        // Create fields for gender (dropdown + optional free-text input)
        const genderLabel = document.createElement('label');
        genderLabel.textContent = `Gender (optional):`;
        elementDetails.appendChild(genderLabel);
        const genderSelect = document.createElement('select');
        genderSelect.name = `gender_${i + 1}`;
        genderSelect.onchange = function() { toggleGenderInput(genderSelect, i + 1); };  // Change handler for "other" selection
        // First option: empty
        const genderEmptyOption = document.createElement('option');
        genderEmptyOption.value = '';
        genderEmptyOption.textContent = '';
        // Second option: feminine
        const feminineOption = document.createElement('option');
        feminineOption.value = 'Feminine';
        feminineOption.textContent = 'Feminine';
        // Third option: neuter
        const neuterOption = document.createElement('option');
        neuterOption.value = 'Neuter';
        neuterOption.textContent = 'Neuter';
        // Fourth option: masculine
        const masculineOption = document.createElement('option');
        masculineOption.value = 'Masculine';
        masculineOption.textContent = 'Masculine';
        // Fifth option: common
        const commonOption = document.createElement('option');
        commonOption.value = 'CommonGender';
        commonOption.textContent = 'Common';
        // Sixth option: vegetable
        const vegetableOption = document.createElement('option');
        vegetableOption.value = 'VegetableGender';
        vegetableOption.textContent = 'Vegetable';
        // Option other
        const genderOtherOption = document.createElement('option');
        genderOtherOption.value = 'other';
        genderOtherOption.textContent = 'Other';
        // Select option
        genderSelect.appendChild(genderEmptyOption);
        genderSelect.appendChild(feminineOption);
        genderSelect.appendChild(neuterOption);
        genderSelect.appendChild(masculineOption);
        genderSelect.appendChild(commonOption);
        genderSelect.appendChild(vegetableOption);
        genderSelect.appendChild(genderOtherOption);
        elementDetails.appendChild(genderSelect);
        // Hidden input for "other" gender (free-text input field)
        const otherGenderInput = document.createElement('input');
        otherGenderInput.type = 'text';
        otherGenderInput.name = `other_gender_${i + 1}`;
        otherGenderInput.placeholder = 'Please specify';
        otherGenderInput.style.display = 'none'; // Hidden by default
        elementDetails.appendChild(otherGenderInput);
        elementDetails.appendChild(document.createElement('br'));
        // Function to toggle free-text input visibility for "other" gender selection
        function toggleGenderInput(selectElement, elementIndex) {
            const otherGenderInput = document.getElementsByName(`other_gender_${elementIndex}`)[0];
            if (selectElement.value === 'other') {
                otherGenderInput.style.display = 'block'; // Show input field when "other" is selected
            } else {
                otherGenderInput.style.display = 'none'; // Hide input field for other selections
            }
        }

        // Create fields for number
        const numberFeaturesLabel = document.createElement('label');
        numberFeaturesLabel.textContent = `Number of the element (optional):`;
        // Create dropdown (select element) for number
        const numberFeaturesSelect = document.createElement('select');
        numberFeaturesSelect.name = `number_${i + 1}`;
        // Populate the dropdown with options from the 'numberFeatures' array
        numberFeatures.forEach(role => {
            const option = document.createElement('option');
            option.value = role;
            option.textContent = role;
            numberFeaturesSelect.appendChild(option);
        });
        // Add "Other" option to the dropdown
        const numberFeaturesOtherOption = document.createElement('option');
        numberFeaturesOtherOption.value = 'Other';
        numberFeaturesOtherOption.textContent = 'Other';
        numberFeaturesSelect.appendChild(numberFeaturesOtherOption);
        // Append the label and dropdown to the container
        elementDetails.appendChild(numberFeaturesLabel);
        elementDetails.appendChild(numberFeaturesSelect);
        elementDetails.appendChild(document.createElement('br'));
        // Create an input field for "Other" option (initially hidden)
        const numberFeaturesOtherInput = document.createElement('input');
        numberFeaturesOtherInput.type = 'text';
        numberFeaturesOtherInput.name = `add_number_${i + 1}`;
        numberFeaturesOtherInput.placeholder = 'Please specify';  // Placeholder text inside the input field
        numberFeaturesOtherInput.style.display = 'none';  // Hidden by default
        // Append the "Other" input field to the container
        elementDetails.appendChild(numberFeaturesOtherInput);
        // Event listener for showing/hiding the "Other" input field based on selection
        numberFeaturesSelect.addEventListener('change', function() {
            if (numberFeaturesSelect.value === 'Other') {
                numberFeaturesOtherInput.style.display = 'inline';  // Show the input field
            } else {
                numberFeaturesOtherInput.style.display = 'none';  // Hide the input field
            }
        });

        // Create fields for case
        const caseFeaturesLabel = document.createElement('label');
        caseFeaturesLabel.textContent = `Case of the element (optional):`;
        // Create dropdown (select element) for case
        const caseFeaturesSelect = document.createElement('select');
        caseFeaturesSelect.name = `case_${i + 1}`;
        // Populate the dropdown with options from the 'caseFeatures' array
        caseFeatures.forEach(role => {
            const option = document.createElement('option');
            option.value = role;
            option.textContent = role;
            caseFeaturesSelect.appendChild(option);
        });
        // Add "Other" option to the dropdown
        const caseFeaturesOtherOption = document.createElement('option');
        caseFeaturesOtherOption.value = 'Other';
        caseFeaturesOtherOption.textContent = 'Other';
        caseFeaturesSelect.appendChild(caseFeaturesOtherOption);
        // Append the label and dropdown to the container
        elementDetails.appendChild(caseFeaturesLabel);
        elementDetails.appendChild(caseFeaturesSelect);
        elementDetails.appendChild(document.createElement('br'));
        // Create an input field for "Other" option (initially hidden)
        const caseFeaturesOtherInput = document.createElement('input');
        caseFeaturesOtherInput.type = 'text';
        caseFeaturesOtherInput.name = `add_case_${i + 1}`;
        caseFeaturesOtherInput.placeholder = 'Please specify';  // Placeholder text inside the input field
        caseFeaturesOtherInput.style.display = 'none';  // Hidden by default
        // Append the "Other" input field to the container
        elementDetails.appendChild(caseFeaturesOtherInput);
        // Event listener for showing/hiding the "Other" input field based on selection
        caseFeaturesSelect.addEventListener('change', function() {
            if (caseFeaturesSelect.value === 'Other') {
                caseFeaturesOtherInput.style.display = 'inline';  // Show the input field
            } else {
                caseFeaturesOtherInput.style.display = 'none';  // Hide the input field
            }
        });

        // Create fields for person (dropdown + optional free-text input)
        const personLabel = document.createElement('label');
        personLabel.textContent = `Person (optional):`;
        elementDetails.appendChild(personLabel);
        const personSelect = document.createElement('select');
        personSelect.name = `person_${i + 1}`;
        personSelect.onchange = function() { togglePersonInput(personSelect, i + 1); };  // Change handler for "other" selection
        // First option: empty
        const personEmptyOption = document.createElement('option');
        personEmptyOption.value = '';
        personEmptyOption.textContent = '';
        // Second option: First
        const firstOption = document.createElement('option');
        firstOption.value = 'first';
        firstOption.textContent = 'First';
        // Third option: Second
        const secondOption = document.createElement('option');
        secondOption.value = 'second';
        secondOption.textContent = 'Second';
        // Fourth option: Third
        const thirdOption = document.createElement('option');
        thirdOption.value = 'third';
        thirdOption.textContent = 'Third';
        // Option other
        const personOtherOption = document.createElement('option');
        personOtherOption.value = 'other';
        personOtherOption.textContent = 'Other';
        // Select option
        personSelect.appendChild(personEmptyOption);
        personSelect.appendChild(firstOption);
        personSelect.appendChild(secondOption);
        personSelect.appendChild(thirdOption);
        personSelect.appendChild(personOtherOption);
        elementDetails.appendChild(personSelect);
        // Hidden input for "other" person (free-text input field)
        const otherPersonInput = document.createElement('input');
        otherPersonInput.type = 'text';
        otherPersonInput.name = `other_person_${i + 1}`;
        otherPersonInput.placeholder = 'Please specify';
        otherPersonInput.style.display = 'none'; // Hidden by default
        elementDetails.appendChild(otherPersonInput);
        elementDetails.appendChild(document.createElement('br'));
        // Function to toggle free-text input visibility for "other" person selection
        function togglePersonInput(selectElement, elementIndex) {
            const otherPersonInput = document.getElementsByName(`other_person_${elementIndex}`)[0];
            if (selectElement.value === 'other') {
                otherPersonInput.style.display = 'block'; // Show input field when "other" is selected
            } else {
                otherPersonInput.style.display = 'none'; // Hide input field for other selections
            }
        }

        // Create a label for the tense selection
        const tenseFeaturesLabel = document.createElement('label');
        tenseFeaturesLabel.textContent = 'Tense of the element (optional):';
        // Create dropdown (select element) for tense
        const tenseFeaturesSelect = document.createElement('select');
        tenseFeaturesSelect.name = `tense_${i + 1}`;
        // Populate the dropdown with options from the 'tenseFeatures' array
        tenseFeatures.forEach(([uri, label]) => {
            const option = document.createElement('option');
            option.value = uri;         // The URI of the tense feature is used as the value
            option.textContent = label; // The label is displayed in the dropdown
            tenseFeaturesSelect.appendChild(option);
        });
        // Add "Other" option to the dropdown
        const tenseFeaturesOtherOption = document.createElement('option');
        tenseFeaturesOtherOption.value = 'Other';
        tenseFeaturesOtherOption.textContent = 'Other';
        tenseFeaturesSelect.appendChild(tenseFeaturesOtherOption);
        // Append the label and dropdown to the container
        elementDetails.appendChild(tenseFeaturesLabel);
        elementDetails.appendChild(tenseFeaturesSelect);
        elementDetails.appendChild(document.createElement('br'));
        // Create an input field for "Other" option (initially hidden)
        const tenseFeaturesOtherInput = document.createElement('input');
        tenseFeaturesOtherInput.type = 'text';
        tenseFeaturesOtherInput.name = `add_tense_${i + 1}`;
        tenseFeaturesOtherInput.placeholder = 'Please specify';  // Placeholder text inside the input field
        tenseFeaturesOtherInput.style.display = 'none';  // Hidden by default
        // Append the "Other" input field to the container
        elementDetails.appendChild(tenseFeaturesOtherInput);
        // Event listener for showing/hiding the "Other" input field based on selection
        tenseFeaturesSelect.addEventListener('change', function() {
            if (tenseFeaturesSelect.value === 'Other') {
                tenseFeaturesOtherInput.style.display = 'inline';  // Show the input field
            } else {
                tenseFeaturesOtherInput.style.display = 'none';  // Hide the input field
            }
        });

        // Create fields for mode
        const modusLabel = document.createElement('label');
        modusLabel.textContent = `(Verb) mode of the element (optional):`;
        // Create dropdown (select element) for mode
        const modusSelect = document.createElement('select');
        modusSelect.name = `modus_${i + 1}`;
        // Populate the dropdown with options from the 'modus' array
        modus.forEach(role => {
            const option = document.createElement('option');
            option.value = role;
            option.textContent = role;
            modusSelect.appendChild(option);
        });
        // Add "Other" option to the dropdown
        const modusOtherOption = document.createElement('option');
        modusOtherOption.value = 'Other';
        modusOtherOption.textContent = 'Other';
        modusSelect.appendChild(modusOtherOption);
        // Append the label and dropdown to the container
        elementDetails.appendChild(modusLabel);
        elementDetails.appendChild(modusSelect);
        elementDetails.appendChild(document.createElement('br'));
        // Create an input field for "Other" option (initially hidden)
        const modusOtherInput = document.createElement('input');
        modusOtherInput.type = 'text';
        modusOtherInput.name = `add_modus_${i + 1}`;
        modusOtherInput.placeholder = 'Please specify';  // Placeholder text inside the input field
        modusOtherInput.style.display = 'none';  // Hidden by default
        // Append the "Other" input field to the container
        elementDetails.appendChild(modusOtherInput);
        // Event listener for showing/hiding the "Other" input field based on selection
        modusSelect.addEventListener('change', function() {
            if (modusSelect.value === 'Other') {
                modusOtherInput.style.display = 'inline';  // Show the input field
            } else {
                modusOtherInput.style.display = 'none';  // Hide the input field
            }
        });

        // Create fields for voice (dropdown + optional free-text input)
        const voiceLabel = document.createElement('label');
        voiceLabel.textContent = `Voice (optional):`;
        elementDetails.appendChild(voiceLabel);
        const voiceSelect = document.createElement('select');
        voiceSelect.name = `voice_${i + 1}`;
        voiceSelect.onchange = function() { toggleVoiceInput(voiceSelect, i + 1); };  // Change handler for "other" selection
        // First option: empty
        const voiceEmptyOption = document.createElement('option');
        voiceEmptyOption.value = '';
        voiceEmptyOption.textContent = '';
        // Second option: Active
        const activeOption = document.createElement('option');
        activeOption.value = 'ActiveVoice';
        activeOption.textContent = 'Active';
        // Third option: Passive
        const passiveOption = document.createElement('option');
        passiveOption.value = 'PassiveVoice';
        passiveOption.textContent = 'Passive';
        // Option other
        const voiceOtherOption = document.createElement('option');
        voiceOtherOption.value = 'other';
        voiceOtherOption.textContent = 'Other';
        // Select option
        voiceSelect.appendChild(voiceEmptyOption);
        voiceSelect.appendChild(activeOption);
        voiceSelect.appendChild(passiveOption);
        voiceSelect.appendChild(voiceOtherOption);
        elementDetails.appendChild(voiceSelect);
        // Hidden input for "other" voice (free-text input field)
        const otherVoiceInput = document.createElement('input');
        otherVoiceInput.type = 'text';
        otherVoiceInput.name = `other_voice_${i + 1}`;
        otherVoiceInput.placeholder = 'Please specify';
        otherVoiceInput.style.display = 'none'; // Hidden by default
        elementDetails.appendChild(otherVoiceInput);
        elementDetails.appendChild(document.createElement('br'));
        // Function to toggle free-text input visibility for "other" voice selection
        function toggleVoiceInput(selectElement, elementIndex) {
            const otherVoiceInput = document.getElementsByName(`other_voice_${elementIndex}`)[0];
            if (selectElement.value === 'other') {
                otherVoiceInput.style.display = 'block'; // Show input field when "other" is selected
            } else {
                otherVoiceInput.style.display = 'none'; // Hide input field for other selections
            }
        }


        // Create fields for semantic property
        const sempropLabel = document.createElement('label');
        sempropLabel.textContent = `Semantic property (optional):`;
        // Create an info icon
        const sempropInfoIcon = document.createElement('span');
        sempropInfoIcon.className = 'info-icon';
        sempropInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const sempropTooltipText = document.createElement('span');
        sempropTooltipText.className = 'tooltiptext';
        sempropTooltipText.innerHTML = `
            Any remarks related to the type of the element which could not be captured by the previous ﬁelds. <br>
            For example: <br>
            The NP often has a very generic meaning, e.g. cose (things, issues). <br>
            AdjP concerns some speciﬁc lexemes that are related to a psychological state.`;
        // Create a container for the label and the info icon
        const sempropLabelContainer = document.createElement('div');
        sempropLabelContainer.className = 'label-container';
        sempropLabelContainer.appendChild(sempropLabel);
        sempropLabelContainer.appendChild(sempropInfoIcon);
        const sempropInput = document.createElement('input');
        sempropInput.type = 'text';
        sempropInput.name = `semprop_${i + 1}`;
        // Create a container for the input and the tooltip
        const sempropTooltipContainer = document.createElement('div');
        sempropTooltipContainer.className = 'tooltip-container';
        sempropTooltipContainer.appendChild(sempropInput);
        sempropTooltipContainer.appendChild(sempropTooltipText);
        // Add tooltip functionality to the info icon
        sempropInfoIcon.appendChild(sempropTooltipText);
        elementDetails.appendChild(sempropLabelContainer);
        elementDetails.appendChild(sempropTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Create fields for other element specification
        const otherElementSpecificationLabel = document.createElement('label');
        otherElementSpecificationLabel.textContent = `Other element specification (optional):`;
        // Create an info icon
        const otherElementSpecificationInfoIcon = document.createElement('span');
        otherElementSpecificationInfoIcon.className = 'info-icon';
        otherElementSpecificationInfoIcon.textContent = 'ℹ️'; // Unicode info symbol
        // Create the tooltip text container with HTML content
        const otherElementSpecificationTooltipText = document.createElement('span');
        otherElementSpecificationTooltipText.className = 'tooltiptext';
        otherElementSpecificationTooltipText.innerHTML = `Any other speciﬁcation that does not ﬁt into the other ﬁelds.`;
        // Create a container for the label and the info icon
        const otherElementSpecificationLabelContainer = document.createElement('div');
        otherElementSpecificationLabelContainer.className = 'label-container';
        otherElementSpecificationLabelContainer.appendChild(otherElementSpecificationLabel);
        otherElementSpecificationLabelContainer.appendChild(otherElementSpecificationInfoIcon);
        const otherElementSpecificationInput = document.createElement('input');
        otherElementSpecificationInput.type = 'text';
        otherElementSpecificationInput.name = `element_specification_${i + 1}`;
        // Create a container for the input and the tooltip
        const otherElementSpecificationTooltipContainer = document.createElement('div');
        otherElementSpecificationTooltipContainer.className = 'tooltip-container';
        otherElementSpecificationTooltipContainer.appendChild(otherElementSpecificationInput);
        otherElementSpecificationTooltipContainer.appendChild(otherElementSpecificationTooltipText);
        // Add tooltip functionality to the info icon
        otherElementSpecificationInfoIcon.appendChild(otherElementSpecificationTooltipText);
        elementDetails.appendChild(otherElementSpecificationLabelContainer);
        elementDetails.appendChild(otherElementSpecificationTooltipContainer);
        elementDetails.appendChild(document.createElement('br'));

        // Add the header and details to the container
        container.appendChild(elementHeader);
        container.appendChild(elementDetails);
    }

    // Dynamically add checkboxes for Topic, Comment, Focus, Background in a grid
    ['Topic', 'Comment', 'Focus', 'Background'].forEach(function(field) {
        const fieldContainer = document.createElement('div');
        const fieldLabel = document.createElement('h4');
        fieldLabel.textContent = `${field}:`;
        fieldContainer.appendChild(fieldLabel);
        for (let i = 0; i < elementNb; i++) {
            const checkboxContainer = document.createElement('div');
            checkboxContainer.className = 'checkbox-container';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = `${constructionName}_${String.fromCharCode(65 + i)}`;
            checkbox.name = `${field.toLowerCase()}_element[]`;
            const checkboxLabel = document.createElement('label');
            checkboxLabel.textContent = `Element ${i + 1}`;
            checkboxContainer.appendChild(checkbox);
            checkboxContainer.appendChild(checkboxLabel);
            fieldContainer.appendChild(checkboxContainer);
        }
        infoContainer.appendChild(fieldContainer);
    });
} // <-- This closes the generateFields function

// Show or hide the details when the header is clicked
function toggleElement(elementNumber) {
    const details = document.getElementById(`elementDetails_${elementNumber}`);
    const icon = document.getElementById(`toggleIcon_${elementNumber}`);
    if (details.style.display === 'none') {
        details.style.display = 'block';
        icon.textContent = '- ';
    } else {
        details.style.display = 'none';
        icon.textContent = '+ ';
    }
}
