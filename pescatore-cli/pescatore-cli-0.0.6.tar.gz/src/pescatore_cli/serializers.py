from rest_framework import serializers


class cerca_stringa_in_bacino__serializer(serializers.Serializer):
    bacino = serializers.CharField(required=True)
    stringa = serializers.CharField(required=True)
    id_licenza = serializers.CharField(required=False)
    id_esca = serializers.CharField(required=False)
    id_consumer = serializers.CharField(required=False)
    note = serializers.CharField(required=False)
    intervallo = serializers.IntegerField(required=False)
