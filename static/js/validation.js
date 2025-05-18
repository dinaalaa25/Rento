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

    // Validate first name
    validateFirstName: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const name = input.value.trim();
        
        if (!name) {
            errorElement.textContent = "First name is required.";
            input.classList.add("error");
            return false;
        }
        
        if (name.length < 3) {
            errorElement.textContent = "First name must be at least 3 characters long.";
            input.classList.add("error");
            return false;
        }

        if (!/^[a-zA-Z\s-']+$/.test(name)) {
            errorElement.textContent = "First name can only contain letters, spaces, hyphens, and apostrophes.";
            input.classList.add("error");
            return false;
        }

        errorElement.textContent = "";
        input.classList.remove("error");
        return true;
    },

    // Validate last name
    validateLastName: function(input) {
        const errorId = input.id + "_error";
        const errorElement = document.getElementById(errorId);
        const name = input.value.trim();
        
        if (!name) {
            errorElement.textContent = "Last name is required.";
            input.classList.add("error");
            return false;
        }
        
        if (name.length < 3) {
            errorElement.textContent = "Last name must be at least 3 characters long.";
            input.classList.add("error");
            return false;
        }

        if (!/^[a-zA-Z\s-']+$/.test(name)) {
            errorElement.textContent = "Last name can only contain letters, spaces, hyphens, and apostrophes.";
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
        const email = input.value.trim();
        
        if (!email) {
            errorElement.textContent = "Email is required.";
            input.classList.add("error");
            return false;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
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
        
        if (!password) {
            errorElement.textContent = "Password is required.";
            input.classList.add("error");
            return false;
        }

        if (password.length < 8) {
            errorElement.textContent = "Password must be at least 8 characters long.";
            input.classList.add("error");
            return false;
        }

        if (!/[A-Za-z]/.test(password)) {
            errorElement.textContent = "Password must contain at least one letter.";
            input.classList.add("error");
            return false;
        }

        if (!/[0-9]/.test(password)) {
            errorElement.textContent = "Password must contain at least one number.";
            input.classList.add("error");
            return false;
        }

        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            errorElement.textContent = "Password must contain at least one special character.";
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
        
        if (!confirmInput.value.trim()) {
            errorElement.textContent = "Please confirm your password.";
            confirmInput.classList.add("error");
            return false;
        }
        
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