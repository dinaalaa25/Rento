// Form validation functions
const validation = {
    // Validate required fields
    validateRequired: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        if (!input.value.trim()) {
            errorElement.textContent = `Please enter the ${input.previousElementSibling.textContent
                .replace(":", "")
                .toLowerCase()}.`;
            input.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate email format
    validateEmail: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!emailRegex.test(input.value.trim())) {
            errorElement.textContent = "Please enter a valid email address.";
            input.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate password strength
    validatePassword: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const password = input.value.trim();
        
        if (password.length < 6) {
            errorElement.textContent = "Password must be at least 6 characters long.";
            input.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate password confirmation
    validatePasswordConfirmation: function(passwordInput, confirmInput) {
        const errorId = confirmInput.id + "_error";
        const errorElement = document.getElementById(errorId);
        
        if (passwordInput.value !== confirmInput.value) {
            errorElement.textContent = "Passwords do not match.";
            confirmInput.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        confirmInput.classList.remove("error");
        return true;
    },

    // Validate number fields
    validateNumber: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const numValue = Number(input.value);
        
        if (isNaN(numValue) || numValue < 0) {
            errorElement.textContent = "Please enter a valid non-negative number.";
            input.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate image URL
    validateImageUrl: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const url = input.value.trim();
        
        if (url && !url.match(/\.(jpeg|jpg|gif|png)$/i)) {
            errorElement.textContent = "Please enter a valid image URL (jpg, jpeg, png, or gif).";
            input.classList.add("error");
            return false;
        }
        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate form with all required validations
    validateForm: function(form) {
        let isValid = true;
        const inputs = form.querySelectorAll("input[required]");

        inputs.forEach((input) => {
            // Check required fields
            if (!this.validateRequired(input)) {
                isValid = false;
            }

            // Apply specific validations based on input type
            switch (input.type) {
                case "email":
                    if (!this.validateEmail(input)) {
                        isValid = false;
                    }
                    break;
                case "password":
                    if (!this.validatePassword(input)) {
                        isValid = false;
                    }
                    // Check password confirmation if it exists
                    if (input.id === "password" && document.getElementById("confirm_password")) {
                        if (!this.validatePasswordConfirmation(input, document.getElementById("confirm_password"))) {
                            isValid = false;
                        }
                    }
                    break;
                case "number":
                    if (!this.validateNumber(input)) {
                        isValid = false;
                    }
                    break;
            }

            // Check for image URL validation
            if (input.id === "car_image") {
                if (!this.validateImageUrl(input)) {
                    isValid = false;
                }
            }
        });

        return isValid;
    }
}; 