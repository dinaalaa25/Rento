//
async function handleSignin(e) {
    e.preventDefault();
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    document
      .querySelectorAll(".error-message")
      .forEach((el) => (el.textContent = ""));

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
        password.value.length < 8 ||
        !/[A-Za-z]/.test(password.value) ||
        !/[0-9]/.test(password.value) ||
        !/[!@#$%^&*(),.?":{}|<>]/.test(password.value)
      ) {
        document.getElementById("password_error").textContent =
          "Password must be at least 8 characters long, contain at least one letter, one number, and one special character.";
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
      }
      else{
        document.getElementById("password_error").textContent =
          "Invalid email or password.";
        return;
      }
    }
  