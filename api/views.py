from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import TimecontrolProfileDateFilter
from api.serializers import TimecontrolSerializer, ProfileCreateSerializer, \
    ProfileSerialize 
from api.utils import post_timecontrol_api_view_response, \
    get_timecontrol_api_view_response
from timecontrolapp.models import Profile, TimeControl


class TimecontrolApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        value = request.data.get('value')
        user = request.user
        return post_timecontrol_api_view_response(user, value)

    def get(self, request, format=None):
        user = request.user
        return get_timecontrol_api_view_response(user)


class TimecontrolListAPIView(generics.ListAPIView):
    serializer_class = TimecontrolSerializer
    permission_classes = [IsAdminUser]
    filterset_class = TimecontrolProfileDateFilter

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = TimeControl.objects.filter(
            profile__company=company).order_by('date')
        return queryset


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        company = self.request.user.profile.company
        serializer.save(company=company)


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        user = instance.user
        user.delete()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = Profile.objects.filter(company=company)
        return queryset
        