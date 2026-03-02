from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Categories,Expenses,Income


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

