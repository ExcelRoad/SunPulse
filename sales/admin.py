from django.contrib import admin
from .models import Lead, Contract


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'lead_number', 
        'contact_name', 
        'lead_source', 
        'status', 
        'estimated_system_size',
        'assigned_to', 
        'city',
        'created_at'
    ]
    list_filter = ['status', 'lead_source', 'assigned_to', 'country', 'is_active']
    search_fields = ['lead_number', 'contact_name', 'email', 'phone', 'city']
    readonly_fields = ['lead_number', 'created_at', 'updated_at']
    raw_id_fields = ['customer', 'assigned_to']
    
    fieldsets = (
        ('פרטי ליד', {
            'fields': ('lead_number', 'lead_source', 'status', 'is_active')
        }),
        ('פרטי התקשרות', {
            'fields': ('contact_name', 'email', 'phone')
        }),
        ('כתובת', {
            'fields': ('street', 'city', 'postal_code', 'country')
        }),
        ('פרטי מערכת', {
            'fields': ('estimated_system_size',)
        }),
        ('שיוך', {
            'fields': ('assigned_to', 'customer')
        }),
        ('נוסף', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_as_contacted', 'mark_as_lost']
    
    @admin.action(description='סמן כ"נוצר קשר"')
    def mark_as_contacted(self, request, queryset):
        from core.constants import LeadStatus
        queryset.update(status=LeadStatus.CONTACTED)
    
    @admin.action(description='סמן כ"אבוד"')
    def mark_as_lost(self, request, queryset):
        from core.constants import LeadStatus
        queryset.update(status=LeadStatus.LOST)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        'contract_number',
        'customer',
        'contract_type',
        'status',
        'start_date',
        'end_date',
        'value',
        'is_expired'
    ]
    list_filter = ['contract_type', 'status', 'is_active']
    search_fields = ['contract_number', 'customer__customer_number', 'customer__company_name']
    readonly_fields = ['contract_number', 'created_at', 'updated_at', 'is_expired']
    raw_id_fields = ['customer']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('פרטי חוזה', {
            'fields': ('contract_number', 'contract_type', 'status', 'is_active')
        }),
        ('קשרים', {
            'fields': ('customer',)
        }),
        ('תנאים', {
            'fields': ('start_date', 'end_date', 'value', 'payment_terms')
        }),
        ('מסמכים', {
            'fields': ('document',)
        }),
        ('נוסף', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def is_expired(self, obj):
        return obj.is_expired
        is_expired.boolean = True
        is_expired.short_description = 'פג תוקף'