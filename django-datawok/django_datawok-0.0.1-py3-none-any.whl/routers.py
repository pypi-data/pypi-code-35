class DatawokRouter:
    """
    A default router you can use to route to a separate datawok database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "datawok":
            return "datawok"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "datawok":
            return "datawok"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == "datawok"
            or obj2._meta.app_label == "datawok"
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "datawok":
            return db == "datawok"
        return None
