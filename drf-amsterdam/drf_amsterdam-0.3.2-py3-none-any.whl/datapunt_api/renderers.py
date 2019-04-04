from rest_framework_csv.renderers import CSVRenderer


class PaginatedCSVRenderer(CSVRenderer):
    results_field = 'results'

    def render(self, data, *args, **kwargs):
        # data = data.limit(30000)
        print(len(data))
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return super(PaginatedCSVRenderer, self).render(data, *args, **kwargs)
