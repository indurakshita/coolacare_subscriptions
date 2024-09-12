from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    object_url = serializers.SerializerMethodField()

    class Meta:
        read_only_fields = ["id", "object_url"]
        abstract = True
        fields = ["object_url"]

    def get_object_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())
