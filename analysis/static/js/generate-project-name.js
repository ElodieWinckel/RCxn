// script for generating the list of projects attached to a specific user

function generateProjectName(uri) {
    const projectSelect = document.getElementById('project-select');
    projectSelect.innerHTML = '<option value="">-- Select a research question --</option>'; // Clear existing options

    const projectIdPrefix = `Project_${uri}`;
    let projectFound = false;

    projects.forEach(([projectId, projectName]) => {
        if (projectId.startsWith(projectIdPrefix)) {
            const option = document.createElement('option');
            option.value = projectId;
            option.textContent = projectName;
            projectSelect.appendChild(option);
            projectFound = true;
        }
    });

        if (!projectFound) {
            projectSelect.innerHTML += '<option value="">No projects found</option>';
        }
}