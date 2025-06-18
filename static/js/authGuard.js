//inside static/js/authGuard.js
document.addEventListener('DOMContentLoaded', function() {
    const authToken = localStorage.getItem('authToken');
    const loginButton = document.getElementById('loginButton');
    const logoutButton = document.getElementById('logoutButton');

    if (authToken) {
        // User is authenticated
        loginButton.style.display = 'none';
        logoutButton.style.display = 'block';
    } else {
        // User is not authenticated
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
    }

    logoutButton.addEventListener('click', function() {
        localStorage.removeItem('authToken');
        window.location.href = '/login'; // Redirect to login page
    });
});

<script src="{{ url_for('static', filename='js/authGuard.js') }}"></script>
