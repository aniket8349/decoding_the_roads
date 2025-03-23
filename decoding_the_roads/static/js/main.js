document.addEventListener("DOMContentLoaded", function() {
  console.log("main.js loaded");
  let darkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.cookie = `theme=${darkMode ? "dark" : "light"}; path=/`;
});