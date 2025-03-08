// JavaScript to toggle active class on button click
document.querySelectorAll('.clicking').forEach(button => {
    button.addEventListener('click', function(event) {
        // Prevent form submission when a button is clicked
        event.preventDefault();
        
        // Remove active class from all buttons
        document.querySelectorAll('.clicking').forEach(btn => btn.classList.remove('active'));
        
        // Add active class to the clicked button
        this.classList.add('active');
    });
});

// Quick emotion analysis function
async function analyzeMood() {
    const text = document.getElementById("text-input").value.trim();
    if (!text) { 
        alert("Please share your thoughts!"); 
        return; 
    }

    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const result = await response.json();
    document.getElementById("result").innerHTML = `
        <p>You feel: <strong>${result.primary_emotion}</strong> with hints of <strong>${result.secondary_emotion}</strong></p>
        <p>Suggestion: ${result.suggestion}</p>
    `;
}

// Function to handle reason selection
function selectReason(reason) {
    // Store the selected reason in the hidden input
    document.getElementById('selected-reason').value = reason;
    
    // Highlight the selected button
    const buttons = document.querySelectorAll('.clicking');
    buttons.forEach(button => {
        if (button.innerText.toLowerCase() === reason) {
            button.classList.add('selected');
        } else {
            button.classList.remove('selected');
        }
    });
}

// Add a class to your CSS for selected buttons
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to reason buttons if not already done in HTML
    const reasonButtons = document.querySelectorAll('.clicking');
    reasonButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reason = this.innerText.toLowerCase();
            selectReason(reason);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const journalForm = document.querySelector('form');
    
    journalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/journal', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Display the emotion results and suggestions
            document.querySelector('.suggestion p').textContent = data.suggestion;
            document.querySelector('.suggestion blockquote').textContent = data.quote;
            document.querySelector('.suggestion .media-links a:first-child').href = data.video_link;
            document.querySelector('.suggestion .media-links a:last-child').href = data.playlist_link;
            
            // Optionally redirect to history
            // window.location.href = '/history';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
