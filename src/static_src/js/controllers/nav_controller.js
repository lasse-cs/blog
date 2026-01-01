import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = [ "button" ]

    toggle() {
        const button = this.buttonTarget;
        const expandedState = button.getAttribute("aria-expanded");
        button.setAttribute("aria-expanded", expandedState === "true" ? "false" : "true");
    }
}