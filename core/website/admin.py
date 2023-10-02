from django.contrib import admin
from .models import Skill, Portfolio, Newsletter, Contact

# Register your models here.

admin.site.register(Skill)


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-'
    list_display = ('title', 'created_date')
    ordering = ('-created_date',)
    search_fields = ('title', 'description')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-'
    list_display = ('name', 'subject', 'created_date', 'email')
    search_fields = ('name', 'subject', 'message', 'email')

# admin.site.register(Post,PostAdmin)  # alterative way of registering
admin.site.register(Newsletter)