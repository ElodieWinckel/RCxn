$(function() {
    $("#metaphoricalExtension").autocomplete({
        source: existingConstructions
    });
});

// Create an empty list of constructions for "Metaphorical extension"
let selectedMetaphoricalExtension = [];

// Populate the list with constructions selected by user
$('#add_metaphorical_extension').click(function() {
    let construction = $('#metaphoricalExtension').val().trim();
    if (construction && !selectedMetaphoricalExtension.includes(construction)) {
        selectedMetaphoricalExtension.push(construction);
        updateSelectedMetaphoricalExtension();
    }
    $('#metaphoricalExtension').val('');  // Clear input field
});

// Display the selected constructions below the field
function updateSelectedMetaphoricalExtension() {
    let selectedMetaphoricalExtensionDiv = $('#selected_metaphorical_extension');
    selectedMetaphoricalExtensionDiv.empty();  // Clear previous buttons
    selectedMetaphoricalExtension.forEach(function(construction, index) {
        let button = $('<button>').text(construction).attr('type', 'button');
        button.click(function() {
            selectedMetaphoricalExtension.splice(index, 1);  // Remove extension list
            updateSelectedMetaphoricalExtension();
        });
        selectedMetaphoricalExtensionDiv.append(button);
    });

// Ensure the hidden input field is updated with an empty list if no constructions are selected
    $('#selected_metaphorical_extension_list').val(selectedMetaphoricalExtension.length ? JSON.stringify(selectedMetaphoricalExtension) : '[]');
}