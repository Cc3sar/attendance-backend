from rest_framework import serializers

from api.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'dpi')