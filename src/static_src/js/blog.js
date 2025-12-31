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