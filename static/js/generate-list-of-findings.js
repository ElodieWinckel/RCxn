// script for generating the list of findings attached to a specific project

function generateFindingsName(Rquestion) {
    const findingsSelect = document.getElementById('findings-select');
    findingsSelect.innerHTML = '<option value="">-- Select a finding --</option>'; // Clear existing options

    const findingsIdPrefix = Rquestion.includes('_F') ? Rquestion : `${Rquestion}_F`;
    let findingsFound = false;

    findings.forEach(([findingsId, findingsName]) => {
        if (findingsId.startsWith(findingsIdPrefix)) {
            const option = document.createElement('option');
            option.value = findingsId;
            option.textContent = findingsName;
            findingsSelect.appendChild(option);
            findingsFound = true;
        }
    });

    // Always add the "Create new findings" option at the end
    const newFindingsOption = document.createElement('option');
    newFindingsOption.value = 'new';
    newFindingsOption.textContent = 'Create new findings';
    findingsSelect.appendChild(newFindingsOption);
}

function toggleFindingsField() {
    const findingsSelect = document.getElementById('findings-select');
    const findingsContainer = document.getElementById('findings-container');

    if (findingsSelect.value === 'new') {
        findingsContainer.style.display = 'block'; // Show text field
    } else {
        findingsContainer.style.display = 'none';  // Hide text field
    }
}
