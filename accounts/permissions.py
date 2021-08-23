from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if (
                request.user.is_staff == False 
                and 
                request.user.is_superuser == False
            ):
            return True

        return False


class IsFacilitator(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if (
                request.user.is_staff == True
                and 
                request.user.is_superuser == False
            ):
            return True

        return False


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if (
                request.user.is_staff == True
                and 
                request.user.is_superuser == True
            ):
            return True

        return False
