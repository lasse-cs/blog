import { Controller } from "@hotwired/stimulus"
import { thresholdFreedmanDiaconis } from "d3";

export default class extends Controller {
    static classes = ["copied"];
    static values = {
        resetDelay: { type: Number, default: 2000 },
    }

    connect() {
        this.timeout = null;
    }

    disconnect() {
        this.clearResetTimeout();
    }

    clearResetTimeout() {
        if (this.timeout) {
            clearTimeout(this.timeout);
            this.timeout = null;
        }
    }

    showCopiedState() {
        this.element.classList.add(this.copiedClass);
        this.clearResetTimeout();

        this.timeout = setTimeout(() => {
            this.element.classList.remove(this.copiedClass);
        }, this.resetDelayValue);
    }

    async copy(event) {
        event.preventDefault();
        try {
            await navigator.clipboard.writeText(window.location.href);
            this.showCopiedState();
        } catch (error) {
            console.log(error);
        }       
    }
}