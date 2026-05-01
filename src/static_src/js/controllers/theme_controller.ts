import { Controller } from "@hotwired/stimulus"

type Theme = "light" | "dark";

export default class extends Controller {
    toggle(event: MouseEvent) {
        const currentTheme = document.documentElement.getAttribute('data-theme') || "light";
        this.setTheme(currentTheme === "dark" ? "light" : "dark", event);
    }

    setTheme(theme: Theme, event: MouseEvent) {
        if (!document.startViewTransition) {
            this.updateTheme(theme);
        } else {
            const button = event.currentTarget as Element;
            const rect = button.getBoundingClientRect();

            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;

            const xPercent = (x / window.innerWidth) * 100;
            const yPercent = (y / window.innerHeight) * 100;

            document.documentElement.style.setProperty("--x", `${xPercent}%`);
            document.documentElement.style.setProperty("--y", `${yPercent}%`);

            document.documentElement.style.viewTransitionName = "theme-switch";
            const transition = document.startViewTransition(() => {
                this.updateTheme(theme);
            })
            transition.finished.finally(() => document.documentElement.style.viewTransitionName = "");
        }

        if (localStorage) {
            localStorage.setItem("theme", theme);
        }
    }

    updateTheme(theme: Theme) {
        if (theme === "dark") {
            document.documentElement.setAttribute("data-theme", theme);
        } else {
            document.documentElement.removeAttribute("data-theme");
        }
    }
}