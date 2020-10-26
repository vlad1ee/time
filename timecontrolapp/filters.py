import django_filters
from django_filters.widgets import RangeWidget

from .models import TimeControl


class TimecontrolDateFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        label='За дату',
        widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control'}))
    date_range = django_filters.DateRangeFilter(label='Или', field_name='date')

    class Meta:
        model = TimeControl
        fields = ['date', ]

    # @property
    # def qs(self):
    #     parent = super().qs
    #     user = self.request.user
    #     company = user.profile.company
    #
    #     return parent.filter(user__company=company)
