// Task.js
function LinkClick(taskId){
    // Show the update overlay
    document.getElementById("update-overlay").style.display = 'block'
    document.getElementById("update-task-div").style.display = 'block'

   // Save the task ID in a hidden input or JavaScript variable
   const updateForm = document.getElementById('update-form-clicker');
   // Set the form action dynamically
   updateForm.action =  `/UpdateTask/${taskId}` 

   // Optionally, populate the input field with the current task name
   const taskName = document.querySelector(`a[onclick*="LinkClick('${taskId}')"]`).closest('tr').querySelector('td').innerText.trim();
   document.getElementById('content').value = taskName;
    
   // Prevent the default link behavior
   return false;}

document.getElementById("update-input").onsubmit = () => {
    document.getElementById("update-overlay").style.display = 'none'
    document.getElementById("update-task-div").style.display = 'none'
    
}

// Skill.js
function LinkClickS(skillId){
    // Show the update overlay
     document.getElementById("update-overlay").style.display = 'block'
     document.getElementById("update-skill-div").style.display = 'block'
 
    // Save the task ID in a hidden input or JavaScript variable
    const updateForm = document.getElementById('update-skill-form');
    // Set the form action dynamically
    const SkillValue = document.getElementById("skill-data").dataset.skillId
    updateForm.action =  `/UpdateSkill/${SkillValue}` 
 
    // Optionally, populate the input field with the current task name
    const taskName = document.querySelector(`a[onclick="LinkClickS(${skillId})"]`).closest('tr').querySelector('td').innerText;
    document.getElementById('update-skill-name').value = taskName;
 
    // Prevent the default link behavior
    return false;}
 
document.getElementById("update-input").onsubmit = () => {
     document.getElementById("update-overlay").style.display = 'none'
     document.getElementById("update-skill-div").style.display = 'none'
     
 }
 
 function AddSpanValue(value){
    document.getElementById("skill-range").textContent = value;
 }


 function UpdateSpanValue(value){
    document.getElementById("skill-range-update").textContent = value;
 }


// Experience.js
 // Function to show the loading overlay
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// Function to hide the loading overlay
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Function to update the loading message
function updateLoadingMessage(message) {
    document.getElementById('loading-message').textContent = message;
}

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('UploadForm');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            // Prevent the default form submission
            event.preventDefault();

            // Show the loading overlay
            loadingOverlay.style.display = 'flex';
            loadingMessage.textContent = 'Uploading your CV...';

            // Create a FormData object from the form
            const formData = new FormData(uploadForm);

            // Send the form data using Fetch API
            fetch(uploadForm.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (response.ok) {
                    // Handle successful upload
                    loadingMessage.textContent = 'Upload complete!';
                } else {
                    // Handle upload error
                    loadingMessage.textContent = 'Upload failed. Please try again.';
                }
            })
            .catch(error => {
                // Handle network error
                loadingMessage.textContent = 'Network error. Please check your connection.';
            })
            .finally(() => {
                // Hide the loading overlay after 2 seconds
                setTimeout(() => {
                    loadingOverlay.style.display = 'none';
                }, 2000);
            });
        });
    }
});