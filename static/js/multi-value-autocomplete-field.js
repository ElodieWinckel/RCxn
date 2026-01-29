/**
 * Generic multi-value field with label, optional tooltip, autocomplete, and JSON hidden input
 *
 * @param {Object} options
 * @param {HTMLElement} options.container
 * @param {number} options.index
 * @param {string} options.labelText
 * @param {string} options.inputId
 * @param {string} options.hiddenInputName
 * @param {Array} options.autocompleteSource
 * @param {string} [options.placeholder]
 * @param {string} [options.tooltipHtml]
 */
function createMultiValueAutocompleteField({
    container,
    index,
    labelText,
    inputId,
    hiddenInputName,
    autocompleteSource,
    placeholder = '',
    tooltipHtml = null
}) {

    // -------------------------------
    // LABEL
    // -------------------------------
    const label = document.createElement('label');
    label.textContent = labelText;

    // -------------------------------
    // OPTIONAL INFO ICON + TOOLTIP
    // -------------------------------
    let labelContainer = label;

    if (tooltipHtml) {
        const infoIcon = document.createElement('span');
        infoIcon.className = 'info-icon';
        infoIcon.textContent = 'ℹ️';

        const tooltipText = document.createElement('span');
        tooltipText.className = 'tooltiptext';
        tooltipText.innerHTML = tooltipHtml;

        const tooltipContainer = document.createElement('div');
        tooltipContainer.className = 'tooltip-container';

        labelContainer = document.createElement('div');
        labelContainer.className = 'label-container';
        labelContainer.appendChild(label);
        labelContainer.appendChild(infoIcon);

        tooltipContainer.appendChild(labelContainer);

        container.appendChild(tooltipContainer);
        container.appendChild(tooltipText);
    } else {
        container.appendChild(label);
    }

    // -------------------------------
    // INPUT
    // -------------------------------
    const input = document.createElement('input');
    input.type = 'text';
    input.id = inputId;
    input.placeholder = placeholder;

    // -------------------------------
    // ADD BUTTON
    // -------------------------------
    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.textContent = 'Add';

    // -------------------------------
    // SELECTED VALUES
    // -------------------------------
    const selectedDiv = document.createElement('div');
    selectedDiv.id = `selected_${inputId}`;

    // -------------------------------
    // HIDDEN INPUT
    // -------------------------------
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = hiddenInputName;
    hiddenInput.value = '[]';

    // -------------------------------
    // DATA MODEL
    // -------------------------------
    let selectedValues = [];

    addBtn.onclick = () => {
        const value = input.value.trim();

        if (value && !selectedValues.includes(value)) {
            selectedValues.push(value);
            render();
        }

        input.value = '';
    };

    function render() {
        selectedDiv.innerHTML = '';

        selectedValues.forEach((val, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.textContent = val;

            btn.onclick = () => {
                selectedValues.splice(idx, 1);
                render();
            };

            selectedDiv.appendChild(btn);
        });

        hiddenInput.value = JSON.stringify(selectedValues);
    }

    // -------------------------------
    // APPEND
    // -------------------------------
    container.appendChild(input);
    container.appendChild(addBtn);
    container.appendChild(selectedDiv);
    container.appendChild(hiddenInput);
    container.appendChild(document.createElement('br'));

    // -------------------------------
    // AUTOCOMPLETE
    // -------------------------------
    $(input).autocomplete({
        source: autocompleteSource
    });
}
