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