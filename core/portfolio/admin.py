from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created_date'
    empty_value_display = '-'
    list_display = ('title', 'created_date')
    ordering = ('-created_date',)
    search_fields = ('title', 'description')

admin.site.register(PortfolioCategory)
# admin.site.register(Post,PostAdmin) # alterative way of registering