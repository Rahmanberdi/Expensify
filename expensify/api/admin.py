from django.contrib import admin
from .models import Expenses,Income,Categories
# Register your models here.

admin.site.register(Categories)
admin.site.register(Expenses)
admin.site.register(Income)
