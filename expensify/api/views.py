from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Categories,Expenses,Income
from .serializers import UserSerializer,CategorySerializer,ExpenseSerializer,IncomeSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateListCategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Categories.objects.filter(Q(user=user)| Q(user__isnull=True))
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class UpdateCategoryView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Categories.objects.filter(user=user)

class DeleteCategoryView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Categories.objects.filter(user=user)
    
class CreateListExpenseView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expenses.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class UpdateExpenseView(generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expenses.objects.filter(user=user)

class DeleteExpenseView(generics.DestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expenses.objects.filter(user=user)

class CreateListIncomeView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class UpdateIncomeView(generics.UpdateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)

class DeleteIncomeView(generics.DestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user=user)
