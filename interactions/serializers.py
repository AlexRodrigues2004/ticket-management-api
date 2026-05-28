from rest_framework import serializers
from .models import Interaction
from users.serializers import UserSerializer


class InteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Interaction
        fields = (
            'id',
            'ticket',
            'user',
            'message',
            'created_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'ticket')


class InteractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ('message',)