// Function to open the login popup
function openLoginForm() {
    document.getElementById('loginPopup').style.display = 'block';
}

// Function to close the login popup
function closeLoginForm() {
    document.getElementById('loginPopup').style.display = 'none';
}

// Function to open the register popup
function openRegisterForm() {
    document.getElementById('registerPopup').style.display = 'block';
}

// Function to close the register popup
function closeRegisterForm() {
    document.getElementById('registerPopup').style.display = 'none';
}

// Close the popup if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('loginPopup')) {
        document.getElementById('loginPopup').style.display = 'none';
    }
    if (event.target == document.getElementById('registerPopup')) {
        document.getElementById('registerPopup').style.display = 'none';
    }
}

// scripts.js
function showMessage() {
    var message = document.getElementById('flashMessage');
    message.style.display = 'block';

    setTimeout(function() {
        message.style.display = 'none';
    }, 3000); // Hide after 3 seconds
}
