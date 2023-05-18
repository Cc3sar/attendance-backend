from rest_framework import serializers

from api.models import Schedule


class ScheduleSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'user', 'entry_datetime', 'exit_datetime')