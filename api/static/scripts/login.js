document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch("http://localhost:8080/auth/token", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'username': username,
            'password': password
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail) });
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            console.log('Login successful, token received:', data.access_token);
            const messageElement = document.getElementById('error-message');
            messageElement.textContent = 'Login successful!';
            messageElement.style.color = 'blue';  // Optional: change message color to green for success
            localStorage.setItem('token', data.access_token);
            setTimeout(() => {
                window.location.href = '/queue';  // Redirect to the queue page
            }, 1000);  // Wait for 1 second before redirecting
        } else {
            document.getElementById('error-message').textContent = 'Username or password incorrect. Try again.';
            messageElement.style.color = 'red';
        }
    })
    .catch(error => {
        document.getElementById('error-message').textContent = `Error: ${error.message}`;
        console.error('Error:', error);
    });
});