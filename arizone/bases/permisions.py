from rest_framework import permissions


class IsBusiness(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if(request.user.permission == "business"):
                return True
        except:
            return False
