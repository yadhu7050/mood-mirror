const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

document.getElementById('loginForm').addEventListener('submit', function(e) {
	e.preventDefault();
	
	const formData = new FormData(this);
	
	fetch('/login', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			window.location.href = data.redirect;
		} else {
			alert(data.message);
		}
	})
	.catch(error => {
		console.error('Error:', error);
		alert('An error occurred. Please try again.');
	});
});

document.getElementById('signupForm').addEventListener('submit', function(e) {
	e.preventDefault();
	
	const formData = new FormData(this);
	
	fetch('/signup', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			window.location.href = data.redirect;
		} else {
			alert(data.message);
		}
	})
	.catch(error => {
		alert('An error occurred. Please try again.');
	});
});