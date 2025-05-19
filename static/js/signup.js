//
async function handleSignup(e) {
  e.preventDefault();

  const first_name = document.getElementById("first_name");
  const last_name = document.getElementById("last_name");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirm_password = document.getElementById("confirm_password");

  // Clear all previous error messages
  document
    .querySelectorAll(".error-message")
    .forEach((el) => (el.textContent = ""));

  // First name validation
  if (first_name.value.trim() === "") {
    document.getElementById("first_name_error").textContent =
      "First name is required.";
    return;
  }

  if (first_name.value.trim().length < 3) {
    document.getElementById("first_name_error").textContent =
      "First name must be at least 3 characters long.";
    return;
  }

  // Last name validation
  if (last_name.value.trim() === "") {
    document.getElementById("last_name_error").textContent =
      "Last name is required.";
    return;
  }

  if (last_name.value.trim().length < 3) {
    document.getElementById("last_name_error").textContent =
      "Last name must be at least 3 characters long.";
    return;
  }

  // Email validation
  if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email.value.trim())) {
    document.getElementById("email_error").textContent =
      "Please enter a valid email address.";
    return;
  }

  // Password validation
  const hasLetter = /[A-Za-z]/.test(password.value);
  const hasNumber = /[0-9]/.test(password.value);
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password.value);
  const isLongEnough = password.value.length >= 8;

  if (!isLongEnough || !hasLetter || !hasNumber || !hasSpecial) {
    document.getElementById("password_error").textContent =
      "Password must be at least 8 characters long and contain letters, numbers, and special characters.";
    return;
  }

  // Confirm password validation
  if (password.value !== confirm_password.value) {
    document.getElementById("confirm_password_error").textContent =
      "Passwords do not match.";
    return;
  }

  try {
    const response = await fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        first_name: first_name.value.trim(),
        last_name: last_name.value.trim(),
        email: email.value.trim(),
        password: password.value
      })
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify(result));
      window.location.href = "/";
    } else {
      document.getElementById("signup_error").textContent = result.message;
    }
  } catch (error) {
    document.getElementById("signup_error").textContent = "An error occurred. Please try again.";
  }
}
