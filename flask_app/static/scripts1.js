function showMessage() {
    var message = document.getElementById('flashMessage');
    message.style.display = 'block';

    setTimeout(function() {
        message.style.display = 'none';
    }, 3000); // Hide after 3 seconds
}

function openLoginForm() {
    document.getElementById('loginPopup').style.display = 'block';
}

function closeLoginForm() {
    document.getElementById('loginPopup').style.display = 'none';
}

function openRegisterForm() {
    document.getElementById('registerPopup').style.display = 'block';
}

function closeRegisterForm() {
    document.getElementById('registerPopup').style.display = 'none';
}