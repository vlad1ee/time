import django_filters

from timecontrolapp.models import TimeControl


class TimecontrolProfileDateFilter(django_filters.FilterSet):
    profile_id = django_filters.NumberFilter(field_name='profile')
    start_date = django_filters.DateFilter(field_name='date',
                                           lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date',
                                           lookup_expr='lte')

    class Meta:
        model = TimeControl
        fields = ['date', 'profile']