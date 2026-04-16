/**
 * Creates a stem/lemma field with tooltip, autocomplete, and multi-value support
 *
 * @param {HTMLElement} container - where the field should be appended
 * @param {number} index - used to generate unique IDs (e.g. i + 1)
 * @param {Array} autocompleteSource - data for jQuery UI autocomplete
 */
function createStemField(container, index, autocompleteSource) {

    // -------------------------------
    // LABEL
    // -------------------------------
    const stemLabel = document.createElement('label');
    stemLabel.textContent = 'Stem / Lemma (optional):';

    // -------------------------------
    // INFO ICON
    // -------------------------------
    const stemInfoIcon = document.createElement('span');
    stemInfoIcon.className = 'info-icon';
    stemInfoIcon.textContent = 'ℹ️';

    // -------------------------------
    // TOOLTIP TEXT
    // -------------------------------
    const stemTooltipText = document.createElement('span');
    stemTooltipText.className = 'tooltiptext';
    stemTooltipText.innerHTML = `
        NB: You probably don't need this field if you entered a surface form above.<br>
        For example:<br>
        English: talk (lemma)<br>
        Spanish: habl- (stem)
    `;

    // -------------------------------
    // INPUT
    // -------------------------------
    const stemInput = document.createElement('input');
    stemInput.type = 'text';
    stemInput.id = `stems_${index}`;
    stemInput.placeholder = 'Type name of lemma';

    // -------------------------------
    // LABEL CONTAINER
    // -------------------------------
    const stemLabelContainer = document.createElement('div');
    stemLabelContainer.className = 'label-container';
    stemLabelContainer.appendChild(stemLabel);
    stemLabelContainer.appendChild(stemInfoIcon);

    // -------------------------------
    // TOOLTIP CONTAINER
    // -------------------------------
    const stemTooltipContainer = document.createElement('div');
    stemTooltipContainer.className = 'tooltip-container';
    stemTooltipContainer.appendChild(stemInput);
    stemTooltipContainer.appendChild(stemTooltipText);

    // -------------------------------
    // ADD BUTTON
    // -------------------------------
    const addStemBtn = document.createElement('button');
    addStemBtn.type = 'button';
    addStemBtn.textContent = 'Add';

    // -------------------------------
    // SELECTED STEMS CONTAINER
    // -------------------------------
    const selectedStemDiv = document.createElement('div');
    selectedStemDiv.id = `selected_stems_${index}`;

    // -------------------------------
    // HIDDEN INPUT (JSON PAYLOAD)
    // -------------------------------
    const hiddenStemInput = document.createElement('input');
    hiddenStemInput.type = 'hidden';
    hiddenStemInput.id = `stems_${index}_hidden`;
    hiddenStemInput.name = `stems_${index}`;

    // -------------------------------
    // DATA MODEL
    // -------------------------------
    let selectedStems = [];

    // -------------------------------
    // ADD BUTTON LOGIC
    // -------------------------------
    addStemBtn.onclick = function () {
        const value = stemInput.value.trim();

        if (value && !selectedStems.includes(value)) {
            selectedStems.push(value);
            updateSelectedStems();
        }

        stemInput.value = '';
    };

    // -------------------------------
    // UPDATE FUNCTION
    // -------------------------------
    function updateSelectedStems() {
        selectedStemDiv.innerHTML = '';

        selectedStems.forEach((stem, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.textContent = stem;

            btn.onclick = function () {
                selectedStems.splice(idx, 1);
                updateSelectedStems();
            };

            selectedStemDiv.appendChild(btn);
        });

        hiddenStemInput.value = selectedStems.length
            ? JSON.stringify(selectedStems)
            : '[]';
    }

    // -------------------------------
    // APPEND EVERYTHING
    // -------------------------------
    container.appendChild(stemLabelContainer);
    container.appendChild(stemTooltipContainer);
    container.appendChild(addStemBtn);
    container.appendChild(selectedStemDiv);
    container.appendChild(hiddenStemInput);
    container.appendChild(document.createElement('br'));

    // -------------------------------
    // AUTOCOMPLETE
    // -------------------------------
    $(`#stems_${index}`).autocomplete({
        source: autocompleteSource
    });

}

