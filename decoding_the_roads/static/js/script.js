const themeToggleBtn = document.getElementById("theme-toggle");
const darkIcon = document.getElementById("theme-toggle-dark-icon");
const lightIcon = document.getElementById("theme-toggle-light-icon");

// Check the saved theme from localStorage
// 
let currentTheme = localStorage.getItem("theme") || "light" 
// window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.classList.toggle("dark", currentTheme === "dark");
updateIcons(currentTheme);

// Function to update icons based on theme
function updateIcons(theme) {
    if (theme === "dark") {
        darkIcon.classList.remove("hidden");
        lightIcon.classList.add("hidden");
    } else {
        darkIcon.classList.add("hidden");
        lightIcon.classList.remove("hidden");
    }
}

// Toggle theme on button click
themeToggleBtn.addEventListener("click", () => {
    currentTheme = document.documentElement.classList.toggle("dark") ? "dark" : "light";
    console.log(currentTheme);
    localStorage.setItem("theme", currentTheme); // Save theme in browser
    updateIcons(currentTheme);
});
