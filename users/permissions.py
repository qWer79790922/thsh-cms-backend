from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    只有 is_staff=True 的管理員可以通過
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsMemberUser(BasePermission):
    """
    一般登入會員（非管理員）可通過
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff