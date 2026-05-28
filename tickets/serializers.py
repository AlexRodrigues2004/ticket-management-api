from rest_framework import serializers
from .models import Ticket
from customers.serializers import CustomerSerializer
from categories.serializers import CategorySerializer
from users.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    created_by_detail = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'title',
            'description',
            'customer',
            'customer_detail',
            'category',
            'category_detail',
            'status',
            'priority',
            'assigned_to',
            'assigned_to_detail',
            'created_by',
            'created_by_detail',
            'opened_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_by', 'opened_at', 'updated_at')


class TicketStatusSerializer(serializers.ModelSerializer):
    """Serializer exclusivo para atualização de status e prioridade pelo atendente."""

    class Meta:
        model = Ticket
        fields = ('status', 'priority', 'assigned_to')