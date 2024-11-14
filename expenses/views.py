from django.shortcuts import render,get_object_or_404
from .serializers import ExpenseSerializer,CategorySerializer
from rest_framework.viewsets import ModelViewSet
from .models import Category,Item
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission
# Create your views here.
class SingleUserAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
"""
CRUD Operations
"""

# best is to use modelviewset that allows crud operations
@permission_classes([IsAdminUser])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
@permission_classes([SingleUserAccess,IsAuthenticated])
class ExpenseViewSet(ModelViewSet):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    serializer_class = ExpenseSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
