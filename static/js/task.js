function LinkClick(taskId){
    // Show the update overlay
    document.getElementById("update-overlay").style.display = 'block'
    document.getElementById("update-content").style.display = 'block'

   // Save the task ID in a hidden input or JavaScript variable
   const updateForm = document.getElementById('update-form-clicker');
   // Set the form action dynamically
   updateForm.action =  `/update/${taskId}` 

   // Optionally, populate the input field with the current task name
   const taskName = document.querySelector(`a[onclick*="LinkClick('${taskId}')"]`).closest('tr').querySelector('td').innerText.trim();
   document.getElementById('content').value = taskName;
    
   // Prevent the default link behavior
   return false;}

document.getElementById("update-input").onsubmit = () => {
    document.getElementById("update-overlay").style.display = 'none'
    document.getElementById("update-content").style.display = 'none'
    
}


