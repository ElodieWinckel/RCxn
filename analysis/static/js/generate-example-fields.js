// A button to create fields for examples
      let exampleCounter = 0;

    function addExample() {
      exampleCounter++;
      const container = document.getElementById('ExamplesContainer');
      const exampleDiv = document.createElement('div');
      exampleDiv.className = 'example';

      // Create the info icon for the "Text of the example" field
      const exampleTextInfoIcon = document.createElement('span');
      exampleTextInfoIcon.className = 'info-icon';
      exampleTextInfoIcon.textContent = 'ℹ️';

      const exampleTextTooltipText = document.createElement('span');
      exampleTextTooltipText.className = 'tooltiptext';
      exampleTextTooltipText.textContent = 'Identify the construction elements with squared brackets, placing the corresponding number right after the closing bracket (no space). For example: [The girl]1 [saw]2 [a strange dog]3.';

      exampleTextInfoIcon.appendChild(exampleTextTooltipText);

      // Create a container for the label and the info icon
      const exampleTextLabelContainer = document.createElement('div');
      exampleTextLabelContainer.className = 'label-container';

      const exampleTextLabel = document.createElement('label');
      exampleTextLabel.htmlFor = `example_text_${exampleCounter}`;
      exampleTextLabel.textContent = 'Text of the example (please use the specific syntax for construction elements for this field):';

      exampleTextLabelContainer.appendChild(exampleTextLabel);
      exampleTextLabelContainer.appendChild(exampleTextInfoIcon);

      // Create the input field for the "Text of the example"
      const exampleTextInput = document.createElement('input');
      exampleTextInput.type = 'text';
      exampleTextInput.id = `example_text_${exampleCounter}`;
      exampleTextInput.name = `example_text_${exampleCounter}`;

      // Create a container for the input and the tooltip
      const exampleTextTooltipContainer = document.createElement('div');
      exampleTextTooltipContainer.className = 'tooltip-container';
      exampleTextTooltipContainer.appendChild(exampleTextInput);

      // Append the "Text of the example" field to the exampleDiv
      exampleDiv.innerHTML = `
          <h3>Example ${exampleCounter}</h3>
      `;
      exampleDiv.appendChild(exampleTextLabelContainer);
      exampleDiv.appendChild(exampleTextInput);
      exampleDiv.appendChild(document.createElement('br'));

      // Append the rest of the fields
      exampleDiv.innerHTML += `
          <label for="example_translation_${exampleCounter}">Translation of the example:</label>
          <input type="text" id="example_translation_${exampleCounter}" name="example_translation_${exampleCounter}">
          <br>
          <label for="example_transliteration_${exampleCounter}">Transliteration of the example:</label>
          <input type="text" id="example_transliteration_${exampleCounter}" name="example_transliteration_${exampleCounter}">
          <br>
          <label for="glosses_${exampleCounter}">Glosses of the example:</label>
          <input type="text" id="glosses_${exampleCounter}" name="glosses_${exampleCounter}">
          <br>
          <label for="comment_${exampleCounter}">Comment:</label>
          <input type="text" id="comment_${exampleCounter}" name="comment_${exampleCounter}">
          <br><br>
      `;

      container.appendChild(exampleDiv);
  }