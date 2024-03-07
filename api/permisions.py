from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAuthenticatedAndIsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_staff)


class IsReviewAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.author
    
