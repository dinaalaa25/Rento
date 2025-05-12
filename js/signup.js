//
document
  .getElementById("signupForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const first_name = document.getElementById("first_name");
    const last_name = document.getElementById("last_name");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirm_password = document.getElementById("confirm_password");

    document
      .querySelectorAll(".error-message")
      .forEach((el) => (el.textContent = ""));

    if (firstName.value.trim() === "") {
      document.getElementById("first_name_error").textContent =
        "First name is required.";
      return;
    }

    if (lastName.value.trim() === "") {
      document.getElementById("last_name_error").textContent =
        "Last name is required.";
      return;
    }

    // Email validation
    if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email.value.trim())) {
      document.getElementById("email_error").textContent =
        "Invalid email address.";
      return;
    }

    if (password.value.length < 8) {
      document.getElementById("password_error").textContent =
        "Password must be at least 8 characters.";
      return;
    }

    if (
      password.length < 8 ||
      !/[A-Za-z]/.test(password) ||
      !/[0-9]/.test(password) ||
      !/[!@#$%^&*(),.?":{}|<>]/.test(password)
    ) {
      document.getElementById("password_error").textContent =
        "Password must be at least 8 characters long, contain at least one letter, one number, and one special character.";
      return;
    }

    if (password.value !== confirmPassword.value) {
      document.getElementById("confirm_password_error").textContent =
        "Passwords do not match.";
      return;
    }

    const response = await fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        password: password.value,
      }),
    });

    const result = await response.json();
    console.log("RESULT", result);

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify(result.user));
    }
    window.location.href = "/";
  });
