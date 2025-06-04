from django.urls import path
from .views import (
    SecuredView, GrantAccessView, RevokeAccessView,
    TransactionListView, TransactionStatsView,
    PredictFraudView, TotalSpentLast5MinView,
    TotalPerUserAndTypeView, TopXProductsView,
    GetDataVersionView, AccessAuditView, ListResourcesView,
    FullTextSearchView, RepushTransactionView, RepushAllTransactionsView
)

urlpatterns = [
    path('secure/', SecuredView.as_view(), name='secure_view'),
    path('access/grant/', GrantAccessView.as_view(), name='grant_access'),
    path('access/revoke/', RevokeAccessView.as_view(), name='revoke_access'),
    path('transactions/', TransactionListView.as_view(), name='transactions_list'),
    path('transactions/stats/', TransactionStatsView.as_view(), name='transactions_stats'),
    path('predict/', PredictFraudView.as_view(), name='predict_fraud'),
    path('metrics/last5min/', TotalSpentLast5MinView.as_view(), name='metrics_last_5min'),
    path('metrics/user-spending/', TotalPerUserAndTypeView.as_view(), name='metrics_user_spending'),
    path('metrics/top-products/<int:x>/', TopXProductsView.as_view(), name='metrics_top_products'),
    path('version/<str:table_name>/<str:version_id>/', GetDataVersionView.as_view(), name='get_data_version'),
    path('audit/<str:table_name>/', AccessAuditView.as_view(), name='access_audit'),
    path('resources/', ListResourcesView.as_view(), name='list_resources'),
    path('search/', FullTextSearchView.as_view(), name='full_text_search'),
    path('repush/<int:transaction_id>/', RepushTransactionView.as_view(), name='repush_transaction'),
    path('repush/all/', RepushAllTransactionsView.as_view(), name='repush_all_transactions'),
]