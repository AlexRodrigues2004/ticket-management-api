from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Interaction
from .serializers import InteractionSerializer, InteractionCreateSerializer
from tickets.models import Ticket


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Interaction.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return InteractionCreateSerializer
        return InteractionSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        serializer.save(user=self.request.user, ticket=ticket)
