
const showMessage = (msg, _class) => {
    document.getElementById('messages').innerHTML = `
    <div class="alert alert-${_class} alert-dismissible fade show" role="alert">
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `
}

const togglePasswords = document.querySelectorAll(".toggle-password");
for (const togglePassword of togglePasswords){
    togglePassword.addEventListener("click", function() {
        const passwordInput = togglePassword.parentElement.parentElement.querySelector('input')
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
        togglePassword.classList.toggle("bi-eye");
    });
}
