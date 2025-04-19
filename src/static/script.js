document.addEventListener("DOMContentLoaded", () => {
    // Ensure the title is always "Paperlit"
    document.title = "Paperlit";

    const signInForm = document.getElementById("sign-in-form");
    const signUpForm = document.getElementById("sign-up-form");
    const showSignUpLink = document.getElementById("show-signup");
    const showSignInLink = document.getElementById("show-signin");

    // Ensure all elements exist
    if (!signInForm || !signUpForm || !showSignUpLink || !showSignInLink) {
        console.error("One or more elements are missing. Check your HTML structure.");
        return;
    }

    // Show sign-in form by default
    signInForm.style.display = "block";
    signUpForm.style.display = "none";

    // Show the sign-up form when "Sign Up" is clicked
    showSignUpLink.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default link behavior
        signInForm.style.display = "none";
        signUpForm.style.display = "block";
    });

    // Show the sign-in form when "Sign In" is clicked
    showSignInLink.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default link behavior
        signInForm.style.display = "block";
        signUpForm.style.display = "none";
    });
});
