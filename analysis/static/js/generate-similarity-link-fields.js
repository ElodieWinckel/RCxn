// A button to create fields for similarity links
let similarityLinkCounter = 0;

function addSimilarityLink() {
    similarityLinkCounter++;
    const container = document.getElementById('SimilarityContainer');
    const similarityLinkDiv = document.createElement('div');
    similarityLinkDiv.className = 'similarityLink';
    similarityLinkDiv.innerHTML = `
        <div class="link-fields">
            <div class="field-group field-half">
                <label for="similarityLink_Cx_${similarityLinkCounter}">Similar construction:</label>
                <input type="text" name="similarityLink_Cx_${similarityLinkCounter}" id="similarityLink_Cx_${similarityLinkCounter}" class="similarityLink_Cx" />
            </div>

            <div class="field-group field-third">
                <label for="crosslinguistic_${similarityLinkCounter}">Crosslinguistic:</label>
                <select name="crosslinguistic_${similarityLinkCounter}" id="crosslinguistic_${similarityLinkCounter}">
                    <option value="Empty"></option>
                    <option value="no">No</option>
                    <option value="yes">Yes</option>
                </select>
            </div>

            <div class="field-group field-third">
                <label for="meaningSim_${similarityLinkCounter}">Meaning sim.:</label>
                <select name="meaningSim_${similarityLinkCounter}" id="meaningSim_${similarityLinkCounter}">
                    <option value="Empty"></option>
                    <option value="Same">Same</option>
                    <option value="Similar">Similar</option>
                    <option value="Different">Different</option>
                </select>
            </div>

            <div class="field-group field-third">
                <label for="formSim_${similarityLinkCounter}">Form sim.:</label>
                <select name="formSim_${similarityLinkCounter}" id="formSim_${similarityLinkCounter}">
                    <option value="Empty"></option>
                    <option value="same">Same</option>
                    <option value="similar">Similar</option>
                    <option value="different">Different</option>
                </select>
            </div>
        </div>
    `;
    container.appendChild(similarityLinkDiv);
    // Apply autocomplete to the newly added input field
    $(`#similarityLink_Cx_${similarityLinkCounter}`).autocomplete({
        source: existingConstructions
    });
}
