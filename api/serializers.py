from rest_framework import serializers
from .models import AccessRight, Transaction, AccessLog

class AccessRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRight
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Transaction
        fields = '__all__'

class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = ['user', 'timestamp', 'method', 'path', 'body', 'resource']