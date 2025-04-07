// Hamburger menu toggle
document.addEventListener("DOMContentLoaded", () => {
    const mobileMenu = document.querySelector(".mobile-menu");
    const navMenu = document.querySelector("nav ul");
  
    if (mobileMenu && navMenu) {
      mobileMenu.addEventListener("click", () => {
        navMenu.classList.toggle("show");
      });
    }
  
    // Form validation
    const form = document.getElementById("contactForm");
    if (form) {
      form.addEventListener("submit", function (e) {
        const name = form.name.value.trim();
        const email = form.email.value.trim();
        const message = form.message.value.trim();
  
        if (!name || !email || !message) {
          alert("Please fill out all fields before submitting.");
          e.preventDefault(); // Stop form from submitting
        } else if (!validateEmail(email)) {
          alert("Please enter a valid email address.");
          e.preventDefault();
        }
      });
    }
  
    function validateEmail(email) {
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return regex.test(email);
    }
  });
  