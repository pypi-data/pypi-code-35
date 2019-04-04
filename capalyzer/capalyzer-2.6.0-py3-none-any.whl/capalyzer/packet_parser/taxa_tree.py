

MY_DEFAULT = 'a_unique_object'


class TaxaTree:


    @attribute
    def rank(self, name):
        """Expose a dictionary mapping names to taxonomic ranks."""
        pass

    @attribute
    def parent(self, name):
        """Expose a dictionary that maps taxa names to their parent."""
        pass

    def generic_rank(self, rank):
        """Return a dict with names going to the given rank."""
        pass

    @attribute
    def kingdom(self, name):
        """Expose a dictionary that maps taxa names to kingdoms."""
        pass

    @attribute
    def phylum(self, name):
        """Expose a dictionary that maps taxa names to phylums."""
        pass
