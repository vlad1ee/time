import datetime

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import TimecontrolProfileDateFilter
from api.serializers import TimecontrolSerializer, ProfileCreateSerializer, \
    ProfileSerializer, TestSerializer
from timecontrolapp.models import Profile, TimeControl


class TimecontrolApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        value = request.data.get('value')
        user = request.user
        if value == 'incoming':
            profile = Profile.objects.get(user=user)
            timecontrol = TimeControl
            TimeControl.objects.create(
                user=profile,
                incoming=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                date=datetime.date.today()
            )
            return Response(status=200)
        elif value == 'outcoming':
            time = TimeControl.objects.filter(profile__user=user).last()
            time.outcoming = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            time.save()
            return Response(status=200)

    def get(self, request, format=None):
        user = request.user
        time_control = TimeControl.objects.filter(profile__user=user,
                                                  date=datetime.date.today())
        if time_control:
            if not time_control.first().outcoming:
                return Response(data={'value': 'outcoming'}, status=200)
            else:
                return Response(data={'value': False}, status=200)
        else:
            return Response(data={'value': 'incoming'}, status=200)


class TimecontrolListAPIView(generics.ListAPIView):
    serializer_class = TimecontrolSerializer
    # permission_classes = [IsAdminUser]
    filterset_class = TimecontrolProfileDateFilter

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = TimeControl.objects.filter(
            profile__company=company).order_by('date')
        return queryset


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = []

    def perform_create(self, serializer):
        company = self.request.user.profile.company
        serializer.save(company=company)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = Profile.objects.filter(company=company)
        return queryset
