import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    '''A filter class for the Message model'''

    # Enables filtering by messages that contain a specific string
    content = django_filters.CharFilter(lookup_expr='icontains')

    # Enable filtering by message within a specific time range
    timestamp = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['content', 'timestamp']

