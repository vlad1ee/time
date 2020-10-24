from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views import generic
from .forms import SignUpForm
from .models import Company, Profile, TimeControl
from django.contrib.auth.decorators import login_required

import datetime


@login_required
def index(request):
    user = request.user
    if user.is_staff:
        return redirect('list')
    if request.method =='POST':
        if request.POST.get('incoming'):
            user = request.user
            profile = Profile.objects.get(user=user)
            TimeControl.objects.create(
                user=profile,
                incoming=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                date=datetime.date.today()
            )
            return redirect('index')
        elif request.POST.get('outcoming'):
            user = request.user
            time = TimeControl.objects.filter(user__user=user).last()
            time.outcoming = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.save()
            return redirect('index')
    user = request.user
    time_control = TimeControl.objects.filter(user__user=user).filter(
        incoming__gte=datetime.date.today())
    if time_control:
        if time_control.last().outcoming:
            time_control = ''
    return render(request, 'index.html', {"time_control": time_control})
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            company = Company.objects.get(name=form.cleaned_data['company'])
            Profile.objects.create(user=user, company=company,
                                   position=form.cleaned_data['position'])
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html', {'form':form})
    if request.user.is_authenticated:
        return redirect('index')
    form = SignUpForm()
    return render(request, 'signup.html', locals())


class TimeControlListView(generic.ListView):
    model = TimeControl
    template_name = 'time_control_list.html'
    extra_context = {}

    def get_queryset(self):
        user = self.request.user
        company = user.profile.company
        queryset = TimeControl.objects.filter(
            user__company=company).order_by('-incoming')
        dates = [i[0] for i in set(queryset.values_list('date'))]
        print(sorted(dates))
        profiles = Profile.objects.filter(company=company)
        res = []
        for profile in profiles:
            timecontrols = queryset.filter(user=profile)
            res.append([profile, timecontrols])
        self.extra_context.update({
            'dates': sorted(dates)
        })
        print(datetime.date.today())
        return res

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return super().get(request, *args, **kwargs)
        return redirect('index')