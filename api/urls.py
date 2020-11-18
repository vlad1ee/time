from django.urls import path, include

from api.views import TimecontrolApiView, TimecontrolListAPIView, \
    ProfileCreateAPIView, ProfileListAPIView

urlpatterns = [
    # path('auth/', include('rest_auth.urls')),
    path('timecontrol/', TimecontrolApiView.as_view()),
    path('timecontrol/list/', TimecontrolListAPIView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('user/create/', ProfileCreateAPIView.as_view()),
    path('user/list/', ProfileListAPIView.as_view()),
    # path('test/', TimecontrolListByProfileAPIView.as_view())
]