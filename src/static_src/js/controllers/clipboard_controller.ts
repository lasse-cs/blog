import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static classes = ["copied"];
    static values = {
        resetDelay: { type: Number, default: 2000 },
    }

    declare readonly copiedClass: string;
    declare readonly resetDelayValue: number;

    private timeout: number | null = null;

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

    async copy(event: Event) {
        event.preventDefault();
        try {
            await navigator.clipboard.writeText(window.location.href);
            this.showCopiedState();
        } catch (error) {
            console.log(error);
        }       
    }
}