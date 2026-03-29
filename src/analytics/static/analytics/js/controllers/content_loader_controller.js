class ContentLoaderController extends window.StimulusModule.Controller {
    static classes = [ "loading" ];
    static values = { url: String };

    connect() {
        this.load();
    }

    load() {
        const loadingTimeout = setTimeout(() => this.element.classList.add(this.loadingClass), 500);
        fetch(this.urlValue)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Request failed with status ${response.status}`);
                }
                return response.json();
            })
            .then(json => {
                this.dispatch("loaded", { detail: { json: json }});
            })
            .catch(error => {
                this.dispatch("failed", {
                    detail: {
                        error: error,
                        message: error.message,
                    },
                });
            })
            .finally(() => {
                clearTimeout(loadingTimeout);
                this.element.classList.remove(this.loadingClass);
            });
    }
}

window.wagtail.app.register("content-loader", ContentLoaderController);