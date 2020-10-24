from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name="profiles")
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class TimeControl(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name="timecontrols")
    incoming = models.DateTimeField()
    outcoming = models.DateTimeField(null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} - {self.incoming} - {self.outcoming}'
