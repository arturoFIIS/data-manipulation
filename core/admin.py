from django.contrib import admin
from .models import User, Company, Customer, Interaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'agent', 'birth_date', 'created_at')
    search_fields = ('name', 'company__name', 'agent__username')
    list_filter = ('company', 'agent', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'type', 'date')
    search_fields = ('customer__name', 'type')
    list_filter = ('type', 'date', 'customer__company')
    readonly_fields = ('date',)