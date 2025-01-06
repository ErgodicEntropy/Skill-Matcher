const API_URL = "http://127.0.0.1:8000/skills";

// Fetch and display skills (GET)
async function fetchSkills() {
    const response = await fetch("http://127.0.0.1:8000/SkillList");
    const skills = await response.json();
    const tableBody = document.querySelector("#skill-table tbody");
    tableBody.innerHTML = skills.map(skill => `
        <tr>
            <td>${skill.id}</td>
            <td>${skill.name}</td>
            <td>${skill.mastery}</td>
            <td>
                <button onclick="editSkill(${skill.id})">Edit</button>
                <button onclick="deleteSkill(${skill.id})">Delete</button>
            </td>
        </tr>
    `).join("");
}

// Add a new skill (POST)
document.getElementById("add-skill-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const newSkill = {
        id: parseInt(document.getElementById("skill-id").value),
        name: document.getElementById("skill-name").value,
        mastery: parseInt(document.getElementById("skill-mastery").value),
    };
    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newSkill),
    });
    fetchSkills();
});

// Delete a skill
async function deleteSkill(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchSkills();
}

// Edit a skill
async function editSkill(id) {
    document.getElementById("update-skill-form").style.display = 'block';    
   // Populate the form with the current skill data (optional)
    const skillToEdit = await fetch(`${API_URL}/${id}`).then(res => res.json());
    document.getElementById("update-skill-name").value = skillToEdit.name;
    document.getElementById("update-skill-mastery").value = skillToEdit.mastery;

    document.getElementById("update-skill-form").addEventListener("submit", async(e) => {
        e.preventDefault()
        const UpdatedSkill = {
            id:id,
            name: document.getElementById("update-skill-name").value,
            mastery: parseInt(document.getElementById("update-skill-mastery").value),
        };

        await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(UpdatedSkill),
        });
        document.getElementById("update-skill-form").style.display = 'none';    
        fetchSkills();
    
        });

    };
// Initial fetch
fetchSkills();
