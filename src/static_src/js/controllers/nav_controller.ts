import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = [ "button" ]

    declare readonly buttonTarget: HTMLButtonElement;

    toggle() {
        const expandedState = this.buttonTarget.getAttribute("aria-expanded");
        this.buttonTarget.setAttribute("aria-expanded", expandedState === "true" ? "false" : "true");
    }
}