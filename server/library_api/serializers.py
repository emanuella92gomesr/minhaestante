from rest_framework import serializers
from library_api.models import LibraryModel


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryModel
        fields = "__all__"
