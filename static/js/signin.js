//
async function handleSignin(e) {
    e.preventDefault();
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    document
      .querySelectorAll(".error-message")
      .forEach((el) => (el.textContent = ""));

    // Basic email format validation
    if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email.value.trim())) {
      document.getElementById("email_error").textContent =
        "Invalid email address.";
      return;
    }

    // Check if fields are not empty
    if (!email.value.trim() || !password.value) {
      document.getElementById("password_error").textContent =
        "Please fill in all fields.";
      return;
    }

    const response = await fetch("/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      localStorage.setItem("user", JSON.stringify(result));
      window.location.href = "/";
    } else {
      document.getElementById("password_error").textContent =
        "Invalid email or password.";
      return;
    }
}
  