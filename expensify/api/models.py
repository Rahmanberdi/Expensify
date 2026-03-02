from django.db import models
from django.contrib.auth.models import User
# Create your models here.
EXPENSES = 'expenses'
INCOME = 'income'


CATEGORY_TYPES = [
    (EXPENSES,'Expenses'),
    (INCOME,'Income')

]


class Categories(models.Model):
    title = models.CharField(max_length=40)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    type = models.CharField(
        max_length = 20,
        choices=CATEGORY_TYPES
    )
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['id']

    def __str__(self):
        return f"{self.title}"
    

class Expenses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type':EXPENSES}
    )
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField()

    class Meta:
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.amount}¥"
    


class Income(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type':INCOME}
    )
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField()

    class Meta:
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f"{self.amount}¥"