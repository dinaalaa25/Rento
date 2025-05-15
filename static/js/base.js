function validateForm(form) {
  const inputs = form.querySelectorAll("input[required]");
  let hasErrors = false;

  inputs.forEach((input) => {
    const errorId = input.id + "_error";
    const errorElement = document.getElementById(errorId);
    if (!input.value.trim()) {
      errorElement.textContent = `Please enter the ${input.previousElementSibling.textContent
        .replace(":", "")
        .toLowerCase()}.`;
      input.classList.add("error");
      hasErrors = true;
    } else {
      errorElement.textContent = "";
      input.classList.remove("error");
    }

    if (input.type === "number") {
      const numValue = Number(input.value);
      if (isNaN(numValue) || numValue < 0) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        errorElement.textContent = "Please enter a valid non-negative number.";
        input.classList.add("error");
        hasErrors = true;
      }
    }

    if (input.type === "file") {
      if (input.value && !/\.(jpe?g|png|gif)$/i.test(input.value)) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        errorElement.textContent =
          "Invalid file type. Please upload a jpg, jpeg, png, or gif image.";
        input.classList.add("error");
        hasErrors = true;
      }
    }
  });

  if (hasErrors) {
    return false; // Prevent form submission
  }
  return true;
}

// Check if user is logged in
function checkUserLoggedIn() {
  // Get current path
  const currentPath = window.location.pathname;
  
  // Skip auth check for signin and signup pages
  if (currentPath === '/signin' || currentPath === '/signup') {
    return;
  }
  
  // Check if user exists in local storage
  const user = localStorage.getItem('user');
  
  if (!user) {
    // If not logged in, redirect to signin page
    window.location.href = '/signin';
  }
}

// Logout function to remove user from local storage and redirect to signin page
function logout() {
  // Remove user data from local storage
  localStorage.removeItem("user");
  
  // Redirect to signin page
  window.location.href = "/signin";
}

// Run auth check when page loads
document.addEventListener('DOMContentLoaded', checkUserLoggedIn);
