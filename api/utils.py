import datetime

from django.utils import timezone
from rest_framework.response import Response

from timecontrolapp.models import TimeControl, Profile


def post_timecontrol_api_view_response(user, value):
    profile = Profile.objects.get(user=user)
    timecontrol = TimeControl.objects.filter(profile=profile,
                                            date=datetime.date.today())
    if value == 'incoming':
        if not timecontrol.exists():
            TimeControl.objects.create(
                profile=profile,
                incoming=timezone.now(),
                date=datetime.date.today()
            )
            return Response(status=200)
    elif value == 'outcoming':
        timecontrol = timecontrol.last()
        if not timecontrol.outcoming:
            timecontrol.outcoming = timezone.now()
            timecontrol.save()
            return Response(status=200)
    return Response(status=400)


def get_timecontrol_api_view_response(user):
    time_control = TimeControl.objects.filter(profile__user=user,
                                              date=datetime.date.today())
    if time_control:
        if not time_control.last().outcoming:
            return Response(data={'value': 'outcoming'}, status=200)
        else:
            return Response(data={'value': False}, status=200)
    else:
        return Response(data={'value': 'incoming'}, status=200)