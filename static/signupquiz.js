let currentQuestionIndex = 0;
const questions = document.querySelectorAll('.question');
const submitButton = document.getElementById('submitButton');

function showQuestion(index) {
    // Hide all questions first
    questions.forEach(q => {
        q.classList.remove('show');
    });

    // Show the current question
    questions[index].classList.add('show');

    // Show submit button on last question
    if (index === questions.length - 1) {
        submitButton.classList.add('show'); // Add 'show' class for animation
        submitButton.style.display = 'block';
    } else {
        submitButton.classList.remove('show');
        submitButton.style.display = 'none';
    }
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        showQuestion(currentQuestionIndex);
    }
}

// Initialize the first question
showQuestion(currentQuestionIndex);

// Move to the next question after a user selection
const options = document.querySelectorAll('.options input');
options.forEach(option => {
    option.addEventListener('change', nextQuestion);
});
