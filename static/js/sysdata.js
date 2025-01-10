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

document.getElementById('RedirectForm').addEventListener('submit', function (event) {
   event.preventDefault(); // Prevent default form submission

   showLoading();
   updateLoadingMessage('Processing your request. Please wait...');

   // Gather all form data (hidden input with None value)
   const formData = new FormData(this);

   // Submit to the /data endpoint
   fetch('/Output', {
       method: 'POST',
       body: formData
   }).then(response => {
       if (response.ok) {
           // Update the loading message
           updateLoadingMessage('Almost there! Thanks for your patience');

       } else {
           console.error('Error submitting to /data:', response.status);
           updateLoadingMessage('Something went wrong. Please try again.');
           hideLoading(); // Hide the loading overlay on error
       }
   }).catch(error => {
       console.error('Error submitting to /data:', error);
       updateLoadingMessage('Something went wrong. Please try again.');
       hideLoading(); // Hide the loading overlay on error
   });
});


// document.getElementById('RedirectForm').addEventListener('submit', function (event) {
//     event.preventDefault(); // Prevent default form submission

//     showLoading();
//     updateLoadingMessage('Almost there! Thanks for your patience');
// });