from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Categories, Expenses, Income
from decimal import Decimal
import datetime

class ExpensifyAPITests(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Create categories for user1
        self.cat_expense = Categories.objects.create(title='Food', user=self.user1, type='expenses')
        self.cat_income = Categories.objects.create(title='Salary', user=self.user1, type='income')
        
        # Global category (user is null)
        self.global_cat = Categories.objects.create(title='Miscellaneous', user=None, type='expenses')

        # Authentication for user1 by default
        self.client.force_authenticate(user=self.user1)

    # --- User Tests ---
    def test_create_user(self):
        url = reverse('create_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        self.client.force_authenticate(user=None) # Ensure no auth required for registration
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

    # --- Category Tests ---
    def test_list_categories(self):
        # user1 should see their own categories AND global categories
        url = reverse('create_list_category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Paginated response
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)

    def test_create_category(self):
        url = reverse('create_list_category')
        data = {'title': 'Travel', 'type': 'expenses'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categories.objects.get(title='Travel').user, self.user1)

    def test_update_category(self):
        url = reverse('update_category', args=[self.cat_expense.id])
        data = {'title': 'Updated Food', 'type': 'expenses'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat_expense.refresh_from_db()
        self.assertEqual(self.cat_expense.title, 'Updated Food')

    def test_delete_category(self):
        url = reverse('delete_category', args=[self.cat_expense.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Categories.objects.filter(id=self.cat_expense.id).exists())

    def test_category_access_control(self):
        # user2 tries to update user1's category
        self.client.force_authenticate(user=self.user2)
        url = reverse('update_category', args=[self.cat_expense.id])
        data = {'title': 'Hacker', 'type': 'expenses'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- Expense Tests ---
    def test_create_expense(self):
        url = reverse('create_list_expenses')
        data = {
            'amount': '50.00',
            'category': self.cat_expense.id,
            'description': 'Lunch',
            'transaction_date': str(datetime.date.today())
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expenses.objects.count(), 1)
        self.assertEqual(Expenses.objects.first().user, self.user1)

    def test_list_expenses(self):
        Expenses.objects.create(user=self.user1, amount=Decimal('10.00'), category=self.cat_expense, transaction_date=datetime.date.today())
        Expenses.objects.create(user=self.user2, amount=Decimal('20.00'), category=self.global_cat, transaction_date=datetime.date.today())
        
        url = reverse('create_list_expenses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user1 should only see their own expense
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['amount'], '10.00')

    def test_update_expense(self):
        expense = Expenses.objects.create(user=self.user1, amount=Decimal('10.00'), category=self.cat_expense, transaction_date=datetime.date.today())
        url = reverse('update_expense', args=[expense.id])
        data = {
            'amount': '15.00',
            'category': self.cat_expense.id,
            'transaction_date': str(datetime.date.today())
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal('15.00'))

    def test_delete_expense(self):
        expense = Expenses.objects.create(user=self.user1, amount=Decimal('10.00'), category=self.cat_expense, transaction_date=datetime.date.today())
        url = reverse('delete_expense', args=[expense.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expenses.objects.filter(id=expense.id).exists())

    # --- Income Tests ---
    def test_create_income(self):
        url = reverse('create_list_income')
        data = {
            'amount': '1000.00',
            'category': self.cat_income.id,
            'description': 'Monthly Salary',
            'transaction_date': str(datetime.date.today())
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.first().user, self.user1)

    def test_list_income(self):
        Income.objects.create(user=self.user1, amount=Decimal('500.00'), category=self.cat_income, transaction_date=datetime.date.today())
        url = reverse('create_list_income')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_income(self):
        income = Income.objects.create(user=self.user1, amount=Decimal('500.00'), category=self.cat_income, transaction_date=datetime.date.today())
        url = reverse('update_income', args=[income.id])
        data = {
            'amount': '600.00',
            'category': self.cat_income.id,
            'transaction_date': str(datetime.date.today())
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        income.refresh_from_db()
        self.assertEqual(income.amount, Decimal('600.00'))

    def test_delete_income(self):
        income = Income.objects.create(user=self.user1, amount=Decimal('500.00'), category=self.cat_income, transaction_date=datetime.date.today())
        url = reverse('delete_income', args=[income.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Income.objects.filter(id=income.id).exists())
