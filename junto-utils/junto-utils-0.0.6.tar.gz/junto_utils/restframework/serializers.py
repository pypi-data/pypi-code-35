from rest_framework import serializers


class ListSerializerBulkUpdate(serializers.ListSerializer):
    """
    Сериалайзер, позволяющий реализовать bulk_update
    """
    read_only_fields = ()

    @staticmethod
    def get_instance_mapping_field(instance):
        return instance.pk

    @staticmethod
    def get_data_mapping_field(data):
        return data['id']

    def update(self, instances, validated_data):
        # Ставим в соответствие:
        # Идентификатор - объект модели
        # Идентификатор - dict из validated_data
        instance_mapping = {
            self.get_instance_mapping_field(instance): instance for instance in instances
        }
        data_mapping = {
            self.get_data_mapping_field(data): data for data in validated_data
        }

        # Соотносим нужные dict из validated_data с нужными объектами моделей
        results = []
        for instance_id, data in data_mapping.items():
            instance = instance_mapping.get(instance_id, None)

            if instance:
                for field in self.read_only_fields:
                    data.pop(field, None)

                # Производим обновление объекта модели
                results.append(self.child.update(instance, data))
        return results
