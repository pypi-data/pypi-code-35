from rest_framework import serializers
from datawok.models import Meta


class MetaSerializer(serializers.ModelSerializer):
    publish_path = serializers.SerializerMethodField()
    publish_link = serializers.SerializerMethodField()
    datawok_model = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_publish_path(self, obj):
        return obj.get_publish_path()

    def get_publish_link(self, obj):
        return obj.get_publish_link()

    def get_datawok_model(self, obj):
        return obj.datawok_model.model

    def get_owner(self, obj):
        return {"id": obj.owner.pk, "name": str(obj.owner)}

    def get_category(self, obj):
        return {"slug": obj.category.slug, "title": str(obj.category)}

    class Meta:
        model = Meta
        fields = "__all__"
