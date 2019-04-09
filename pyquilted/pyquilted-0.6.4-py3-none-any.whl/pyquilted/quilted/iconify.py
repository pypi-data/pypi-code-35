class Iconify:
    def iconify(self, value=None, default=None):
        if value:
            return 'fa-' + value
        return default
