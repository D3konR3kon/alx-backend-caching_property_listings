from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'formatted_price', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Property Details', {
            'fields': ('price', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_price(self, obj):
        return obj.formatted_price()
    formatted_price.short_description = 'Price'