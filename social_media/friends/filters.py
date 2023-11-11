import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserFilterSet(django_filters.FilterSet):
    query = django_filters.CharFilter(method="user_filter", label="Search")

    class Meta:
        model = User
        fields = ["query"]

    def user_filter(self, queryset, name, value):
        return queryset.filter(
            Q(email__iexact=value)
            | Q(first_name__icontains=value)
        )
