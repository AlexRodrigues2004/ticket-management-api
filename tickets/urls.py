from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from .views import TicketViewSet
from interactions.views import InteractionViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

tickets_router = nested_routers.NestedDefaultRouter(router, r'tickets', lookup='ticket')
tickets_router.register(r'interactions', InteractionViewSet, basename='ticket-interactions')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tickets_router.urls)),
]
