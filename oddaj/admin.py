from django.contrib import admin
from .models import Category, Institution, Donation
# Register your models here.

admin.site.register(Category)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'typ')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'institution', 'is_taken')