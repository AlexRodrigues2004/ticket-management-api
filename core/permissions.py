from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAttendant(BasePermission):
    """Permite acesso apenas a atendentes e administradores."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('atendente', 'admin')


class IsAdminUser(BasePermission):
    """Permite acesso apenas a administradores."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerCustomer(BasePermission):
    """
    Cliente só acessa seus próprios chamados.
    Atendentes e admins acessam tudo.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role in ('atendente', 'admin'):
            return True
        # obj é um Ticket — verifica se o customer está vinculado ao user
        return obj.created_by == request.user