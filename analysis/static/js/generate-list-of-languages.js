$(function() {
    $('#treeDropdown').jstree({
        "core": {
            "data": {
                "url": languageTreeUrl,  // constant defined in html file
                "dataType": "json"
            }
        }
    });

    // Save selection to hidden field
    $('#treeDropdown').on("select_node.jstree", function (e, data) {
        $("#language").val(data.node.id);       // store the URI
        $("#language_label").val(data.node.text); // store the label
    });
});
