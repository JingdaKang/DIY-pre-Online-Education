from rest_framework import serializers

from user.serializers import UserSerializer, TeamSerializer


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    recipient = UserSerializer(read_only=True)
    unread = serializers.BooleanField(read_only=True)
    verb = serializers.CharField(read_only=True)
    target = TeamSerializer(read_only=True)
    actor = UserSerializer(read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")