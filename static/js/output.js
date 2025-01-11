let timers = {};

function startTimer(taskId) {
    const startTime = Date.now();
    timers[taskId] = startTime;

    const timerDisplay = document.createElement('span');
    timerDisplay.id = 'timer-' + taskId;
    timerDisplay.style.marginLeft = '10px';
    document.getElementById('task-' + taskId).appendChild(timerDisplay);

    updateTimer(taskId);
}

function updateTimer(taskId) {
    const timerDisplay = document.getElementById('timer-' + taskId);
    if (!timerDisplay) return;

    const elapsedTime = Date.now() - timers[taskId];
    const seconds = Math.floor((elapsedTime / 1000) % 60);
    const minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
    const hours = Math.floor((elapsedTime / (1000 * 60 * 60)) % 24);

    timerDisplay.innerHTML = `${hours}h ${minutes}m ${seconds}s`;

    setTimeout(() => updateTimer(taskId), 1000);
}

function stopTimer(taskId) {
    delete timers[taskId];
    const timerDisplay = document.getElementById('timer-' + taskId);
    if (timerDisplay) {
        timerDisplay.remove();
    }
}

function markAsDoing(taskId) {
    const taskRow = document.getElementById('task-' + taskId);
    const taskContent = taskRow.querySelector('td');

    taskRow.classList.add('doing');
    taskContent.classList.add('almost_completed');

    const doingButton = taskRow.querySelector('.doing-button');
    doingButton.innerHTML = 'Doing';
    doingButton.style.backgroundColor = '#808080';
    doingButton.style.cursor = 'not-allowed';

    startTimer(taskId);
}
function openFeedbackModal(taskId){
    const overlay = document.getElementById("overlay");
    const modal = document.getElementById("feedbackModal");
    overlay.style.display = "block";        
    modal.style.display = "block";
    

    // Save taskId in a hidden field or as a global variable
    modal.dataset.taskId = taskId;

}

function submitFeedback() {
    const modal = document.getElementById("feedbackModal");

    const taskId = modal.dataset.taskId;
    const feedback = document.querySelector('input[name="feedback"]:checked');
    
    if (feedback) {
        saveFeedback(taskId, feedback.value);
        closeModal();
    } else {
        alert("Please select a feedback option.");
    }
}

function saveFeedback(taskId, feedback) {
    console.log(`Task ID: ${taskId}, Feedback: ${feedback}`);

    fetch('/save_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ taskId: taskId, feedback: feedback }),
    })
    .then(response => {
        if (response.ok) {
            return response.blob(); // Receive the file as a blob
        }
        throw new Error('Failed to save feedback');
    })
    .then(blob => {
        // Create a link element and trigger the download
        const link = document.createElement('a');
        const url = window.URL.createObjectURL(blob);
        link.href = url;
        link.download = 'feedback.json'; // Default file name for the downloaded file
        link.click(); // Trigger the download
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function closeModal() {
    const modal = document.getElementById("feedbackModal");
    const overlay = document.getElementById("overlay");
    modal.style.display = "none";
    overlay.style.display = "none";
}
    
function markAsFinished(taskId) {
    const taskRow = document.getElementById('task-' + taskId);
    const taskContent = taskRow.querySelector('td');

    taskRow.classList.add('finished');
    taskContent.classList.add('completed');
    
    const finishButton = taskRow.querySelector('.finish-button');
    finishButton.innerHTML = 'Completed';
    finishButton.style.backgroundColor = '#808080';
    finishButton.style.cursor = 'not-allowed';

    stopTimer(taskId);
    openFeedbackModal(taskId);
}

