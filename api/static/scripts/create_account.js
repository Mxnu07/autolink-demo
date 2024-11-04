document.getElementById('create-account-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('https://autolinkservice.co/user/create_account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "User created successfully") {
            const messageElement = document.getElementById('message');
            messageElement.textContent = 'User created successfully';
            messageElement.style.color = 'blue';  // Optional: change message color to green for success
            setTimeout(() => {
                window.location.href = '/login';
            }, 1000);  // Wait for 1 second before redirecting
        } else {
            document.getElementById('message').textContent = 'Error creating account. Try again.';
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error creating account. Try again.';
        console.error('Error:', error);
    });
});
