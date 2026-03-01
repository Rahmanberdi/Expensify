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

urlpatterns = [
    path('category/create/',CreateListCategoryView.as_view(),name='create_list_category'),
    path('category/delete/<int:pk>/',DeleteCategoryView.as_view(),name='delete_category'),
    path('category/update/<int:pk>/',UpdateCategoryView.as_view(),name='update_category')
]
