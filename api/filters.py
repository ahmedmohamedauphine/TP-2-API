from django_filters import rest_framework as filters
from .models import Transaction

class TransactionFilter(filters.FilterSet):
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr='gt')
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr='lt')
    amount = filters.NumberFilter(field_name="amount", lookup_expr='exact')

    customer_rating__gt = filters.NumberFilter(field_name="customer_rating", lookup_expr='gt')
    customer_rating__lt = filters.NumberFilter(field_name="customer_rating", lookup_expr='lt')
    customer_rating = filters.NumberFilter(field_name="customer_rating", lookup_expr='exact')

    product_name = filters.CharFilter(lookup_expr='icontains')
    product_category = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    status = filters.CharFilter(lookup_expr='exact')
    payment_method = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Transaction
        fields = []