const navToggle = document.querySelector('[aria-controls="main-nav"]');
const primaryNav = document.querySelector('#main-nav');

navToggle.addEventListener("click", () => {
    const navOpened = navToggle.getAttribute("aria-expanded");
    if (navOpened === "false") {
        navToggle.setAttribute("aria-expanded", "true");
    } else {
        navToggle.setAttribute("aria-expanded", "false");
    }
});

const themeToggle = document.querySelector('#theme-toggle');

themeToggle.addEventListener("click", () => { 
    const currentTheme = document.documentElement.getAttribute('data-theme') || "light";
    if (currentTheme === "light") {
        document.documentElement.setAttribute("data-theme", "dark");
    } else {
        document.documentElement.removeAttribute("data-theme");
    }
});