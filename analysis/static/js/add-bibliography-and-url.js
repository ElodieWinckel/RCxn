        $(document).ready(function() {
    // Add new literature entry
    $('#add-literature-btn').click(function() {
      const newEntry = `
        <div class="literature-entry">
          <label for="literature">Add RDF code for literature reference:</label>
          <textarea name="literature[]" rows="5" cols="50" placeholder="Paste RDF code"></textarea>
        </div>`;
      $('#literature-container').append(newEntry);
    });

    // Add new URL entry
    $('#add-url-btn').click(function() {
      const newUrlEntry = `
        <div class="url-entry">
          <label for="url">Please provide an URL:</label>
          <input type="url" name="url[]" placeholder="Enter URL">
        </div>`;
      $('#url-container').append(newUrlEntry);
    });
  });