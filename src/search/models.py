class SearchItemPageMixin:
    def get_search_summary_template(self):
        if hasattr(self, "search_summary_template"):
            return self.search_summary_tempate
        if hasattr(self, "summary_template"):
            return self.summary_template
        raise NotImplementedError("You must define summary_template on the model.")
