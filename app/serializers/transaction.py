from django.db.models import Q
from rest_framework import serializers, viewsets
from app.models.transaction import Transaction
from app.serializers.category import CategorySerializer
from app.serializers.account import AccountSerializer

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
