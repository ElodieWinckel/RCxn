$(function() {
    $("#inheritsFrom").autocomplete({
        source: existingConstructions
    });
});

// Create an empty list of constructions for "Inherits from"
    let selectedInheritsFrom = [];

// Populate the list with constructions selected by user
$('#add_inherits_from').click(function() {
    let construction = $('#inheritsFrom').val().trim();
    if (construction && !selectedInheritsFrom.includes(construction)) {
        selectedInheritsFrom.push(construction);
        updateSelectedInheritsFrom();
    }
    $('#inheritsFrom').val('');  // Clear input field
});

// Display the selected constructions below the field
function updateSelectedInheritsFrom() {
    let selectedInheritsFromDiv = $('#selected_inherits_from');
    selectedInheritsFromDiv.empty();  // Clear previous buttons
    selectedInheritsFrom.forEach(function(construction, index) {
        let button = $('<button>').text(construction).attr('type', 'button');
        button.click(function() {
            selectedInheritsFrom.splice(index, 1);  // Remove from list
            updateSelectedInheritsFrom();
        });
        selectedInheritsFromDiv.append(button);
    });

    // Ensure the hidden input field is updated with an empty list if no constructions are selected
    $('#selected_inherits_from_list').val(selectedInheritsFrom.length ? JSON.stringify(selectedInheritsFrom) : '[]');
}