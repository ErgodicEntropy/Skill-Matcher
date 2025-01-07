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
    const taskName = document.querySelector(`a[onclick="LinkClick(${skillId})"]`).closest('tr').querySelector('td').innerText;
    document.getElementById('update-skill-name').value = taskName;
 
    // Prevent the default link behavior
    return false;}
 
 document.getElementById("update-input").onsubmit = () => {
     document.getElementById("update-overlay").style.display = 'none'
     document.getElementById("update-content").style.display = 'none'
     
 }
 
 function AddSpanValue(value){
    document.getElementById("skill-range").textContent = value;
 }


 function UpdateSpanValue(value){
    document.getElementById("skill-range-update").textContent = value;
 }