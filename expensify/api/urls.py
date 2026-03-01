"""
URL configuration for expensify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from api.views import CreateListCategoryView,DeleteCategoryView,UpdateCategoryView
from api.views import CreateListExpenseView,DeleteExpenseView,UpdateExpenseView
from api.views import CreateListIncomeView, DeleteIncomeView, UpdateIncomeView
urlpatterns = [
    path('category/create/',CreateListCategoryView.as_view(),name='create_list_category'),
    path('category/delete/<int:pk>/',DeleteCategoryView.as_view(),name='delete_category'),
    path('category/update/<int:pk>/',UpdateCategoryView.as_view(),name='update_category'),

    path('expense/create/',CreateListExpenseView.as_view(),name='create_list_expenses'),
    path('expense/delete/<int:pk>/',DeleteExpenseView.as_view(),name='delete_expense'),
    path('expense/update/<int:pk>/',UpdateExpenseView.as_view(),name='update_expense'),
    
    path('income/create/',CreateListIncomeView.as_view(),name='create_list_income'),
    path('income/delete/<int:pk>/',DeleteIncomeView.as_view(),name='delete_income'),
    path('income/update/<int:pk>/',UpdateIncomeView.as_view(),name='update_income'),
]
