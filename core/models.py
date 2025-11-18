from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'core_user'

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Companies'

class Customer(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['company', 'agent']),
        ]

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Meeting', 'Meeting'),
        ('Facebook', 'Facebook'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    date = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['customer', '-date']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.customer.name} - {self.type}"