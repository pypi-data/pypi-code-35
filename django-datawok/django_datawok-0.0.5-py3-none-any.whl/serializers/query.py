from rest_framework import serializers
from datawok.models import Query


class QuerySerializer(serializers.ModelSerializer):
    datawok_model = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()

    def get_datawok_model(self, obj):
        return str(obj.datawok_model)

    def get_creator(self, obj):
        return {"id": obj.creator.pk, "title": str(obj.creator)}

    class Meta:
        model = Query
        fields = "__all__"
