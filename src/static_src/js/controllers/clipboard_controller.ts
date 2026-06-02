import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
    static targets = ["source"];
    static classes = ["copied"];
    static values = {
        resetDelay: { type: Number, default: 2000 },
    }

    declare readonly hasSourceTarget: boolean;
    declare readonly sourceTarget: HTMLElement;
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
            const text = this.hasSourceTarget
                ? this.sourceTarget.textContent ?? ""
                : window.location.href;

            await navigator.clipboard.writeText(text);
            this.showCopiedState();
        } catch (error) {
            console.log(error);
        }
    }
}
