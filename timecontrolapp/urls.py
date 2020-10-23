from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('list/', TimeControlListView.as_view(), name='list'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view()),
]