from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAuthenticatedAndIsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow all GET requests (read-only)
        if request.method in SAFE_METHODS:
            return True
        # Check if the user is authenticated and is an admin user
        return bool(request.user and request.user.is_staff)

# In this custom permission class:
# - The has_permission method checks if the request method is a safe method (GET, HEAD, OPTIONS) and allows it without any further checks.
# - For other methods (POST, PUT, PATCH, DELETE), it checks if the user is authenticated and is an admin user (is_staff attribute is True).

class IsReviewAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests for all users
        if request.method in SAFE_METHODS:
            return True
        # Check if the user is the author of the review
        return request.user == obj.author
    
# In this custom permission class:
# - The has_object_permission method checks if the request method is a safe method (GET, HEAD, OPTIONS) and allows it without any further checks.
# - For other methods (PUT, PATCH, DELETE), it checks if the user making the request is the author of the review being accessed.
