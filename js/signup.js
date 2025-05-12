// 
document.getElementById("signupForm").addEventListener("submit", function (e) {
  const firstName = document.getElementById("firstName");
  const lastName = document.getElementById("lastName");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");

  let valid = true;

  // Clear previous errors
  document
    .querySelectorAll(".error-message")
    .forEach((el) => (el.textContent = ""));

  if (firstName.value.trim() === "") {
    document.getElementById("firstNameError").textContent =
      "First name is required.";
    valid = false;
  }

  if (lastName.value.trim() === "") {
    document.getElementById("lastNameError").textContent =
      "Last name is required.";
    valid = false;
  }

  if (!email.value.includes("@")) {
    document.getElementById("emailError").textContent =
      "Invalid email address.";
    valid = false;
  }

  if (password.value.length < 6) {
    document.getElementById("passwordError").textContent =
      "Password must be at least 6 characters.";
    valid = false;
  }

  if (password.value !== confirmPassword.value) {
    document.getElementById("confirmPasswordError").textContent =
      "Passwords do not match.";
    valid = false;
  }

  if (!valid) {
    e.preventDefault(); // Prevent form submission
  }
});
