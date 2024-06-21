document.getElementById('userForm').addEventListener('submit', function() {
    var errorDiv = document.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
    document.getElementById('loader').style.display = 'block';
});
