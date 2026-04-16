$(function() {
    $("#inheritedBy").autocomplete({
        source: existingConstructions
    });
});

// Create an empty list of constructions for "Inherited by"
let selectedInheritedBy = [];

// Populate the list with constructions selected by user
$('#add_inherited_by').click(function() {
    let construction = $('#inheritedBy').val().trim();
        if (construction && !selectedInheritedBy.includes(construction)) {
            selectedInheritedBy.push(construction);
            updateSelectedInheritedBy();
        }
    $('#inheritedBy').val('');  // Clear input field
});

// Display the selected constructions below the field
function updateSelectedInheritedBy() {
    let selectedInheritedByDiv = $('#selected_inherited_by');
    selectedInheritedByDiv.empty();  // Clear previous buttons
    selectedInheritedBy.forEach(function(construction, index) {
        let button = $('<button>').text(construction).attr('type', 'button');
        button.click(function() {
            selectedInheritedBy.splice(index, 1);  // Remove by list
            updateSelectedInheritedBy();
        });
        selectedInheritedByDiv.append(button);
    });

// Ensure the hidden input field is updated with an empty list if no constructions are selected
    $('#selected_inherited_by_list').val(selectedInheritedBy.length ? JSON.stringify(selectedInheritedBy) : '[]');
}