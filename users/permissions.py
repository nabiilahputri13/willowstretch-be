from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Izin ini strict: Cuma boleh kalau Login DAN Role-nya Admin
        return bool(
            request.user and request.user.is_authenticated and request.user.is_admin
        )
