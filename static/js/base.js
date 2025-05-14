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

// TODO: add a function to logout and redirect to the login page
