from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Sum, Q
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from kafka import KafkaProducer
import pickle
import numpy as np
import json

from .models import AccessRight, Transaction, AccessLog
from .serializers import AccessRightSerializer, TransactionSerializer, AccessLogSerializer
from .filters import TransactionFilter

class SecuredView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        table_name = "transactions"
        if AccessRight.objects.filter(user=request.user, table_name=table_name, can_access=True).exists():
            return Response({"message": f"Accès autorisé à {table_name}"})
        return Response({"error": "Accès refusé"}, status=403)

class GrantAccessView(APIView):
    def post(self, request):
        serializer = AccessRightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RevokeAccessView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            access = AccessRight.objects.get(user=user, table_name=request.data['table_name'])
            access.delete()
            return Response({"message": "Access revoked"}, status=200)
        except AccessRight.DoesNotExist:
            return Response({"error": "Access not found"}, status=404)

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        if not AccessRight.objects.filter(user=user, table_name="transactions", can_access=True).exists():
            raise PermissionDenied("Access to 'transactions' is denied.")
        return Transaction.objects.all()

    def get_serializer(self, *args, **kwargs):
        fields_param = self.request.query_params.get('fields')
        if fields_param:
            fields = fields_param.split(',')
            kwargs['fields'] = fields
        return self.serializer_class(*args, **kwargs)

class TransactionStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not AccessRight.objects.filter(user=request.user, table_name="transactions", can_access=True).exists():
            raise PermissionDenied("Access denied.")
        data = {
            "count": Transaction.objects.count(),
            "average_amount": Transaction.objects.aggregate(Avg('amount'))['amount__avg']
        }
        return Response(data)

class TotalSpentLast5MinView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        five_minutes_ago = now() - timedelta(minutes=5)
        total = Transaction.objects.filter(created_at__gte=five_minutes_ago).aggregate(Sum('amount'))['amount__sum']
        return Response({"total_spent_last_5_min": total or 0})

class TotalPerUserAndTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = Transaction.objects.values('customer__username', 'payment_method').annotate(total=Sum('amount')).order_by('-total')
        return Response(list(results))

class TopXProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, x):
        results = Transaction.objects.values('product_name').annotate(count=Count('id')).order_by('-count')[:x]
        return Response(list(results))

class GetDataVersionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, table_name, version_id):
        return Response({"error": f"Versioning not implemented for table '{table_name}'"}, status=501)

class AccessAuditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, table_name):
        logs = AccessLog.objects.filter(resource__icontains=table_name).order_by('-timestamp')
        serializer = AccessLogSerializer(logs, many=True)
        return Response(serializer.data)

class ListResourcesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"resources": ["transactions", "users", "logs"]})

class FullTextSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Missing search query (?q=...)"}, status=400)

        results = Transaction.objects.filter(
            Q(product_name__icontains=query) |
            Q(product_category__icontains=query) |
            Q(status__icontains=query) |
            Q(country__icontains=query)
        )
        serializer = TransactionSerializer(results, many=True)
        return Response(serializer.data)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class RepushTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
            tx_data = {
                "id": tx.id,
                "product_name": tx.product_name,
                "amount": tx.amount,
                "timestamp": now().isoformat()
            }
            producer.send('transactions', tx_data)
            return Response({"message": "Transaction pushed to Kafka"})
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

class RepushAllTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        txs = Transaction.objects.all()
        for tx in txs:
            tx_data = {
                "id": tx.id,
                "product_name": tx.product_name,
                "amount": tx.amount,
                "timestamp": now().isoformat()
            }
            producer.send('transactions', tx_data)
        return Response({"message": "All transactions pushed to Kafka"})

class PredictFraudView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with open("api/model.pkl", "rb") as f:
                model = pickle.load(f)
            features = request.data.get("features")
            if not features:
                return Response({"error": "Missing 'features' in request"}, status=400)
            prediction = model.predict([features])[0]
            return Response({"prediction": int(prediction)})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
