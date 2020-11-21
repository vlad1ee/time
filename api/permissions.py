from django.utils import timezone
from rest_framework import permissions


class SubscribtionIsActive(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        if profile.subscription and profile.subscription >= timezone.now():
            return True
        return False
