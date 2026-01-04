from django.db.models import Q
from rest_framework import serializers, viewsets
from app.models.transaction import Transaction
from app.serializers.category import CategorySerializer
from app.serializers.account import AccountSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    receiver = AccountSerializer()
    sender = AccountSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'comment', 'category', 'create_at']

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.all().order_by('id') if user.is_staff else Transaction.objects.filter(Q(sender__owners=user) | Q(receiver__owners=user)).distinct().order_by('id')

    @action(detail=False, url_path='by_account/(?P<account_id>[^/.]+)')
    def by_account(self, request, account_id=None):
        queryset = self.get_queryset().filter(
            Q(sender_id=account_id) | Q(receiver_id=account_id)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
