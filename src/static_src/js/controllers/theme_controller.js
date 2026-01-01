import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    toggle() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || "light";
        this.setTheme(currentTheme === "dark" ? "light" : "dark");
    }

    setTheme(theme) {
        if (theme === "dark") {
            document.documentElement.setAttribute("data-theme", theme);
        } else {
            document.documentElement.removeAttribute("data-theme");
        }

        if (localStorage) {
            localStorage.setItem("theme", theme);
        }
    }
}