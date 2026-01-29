from django.contrib import admin
from .models import Customer, Contact, Installer, Supplier


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1
    fields = ['first_name', 'last_name', 'role', 'email', 'phone', 'is_primary']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_number', 'display_name', 'customer_type', 'city', 'phone', 'is_active']
    list_filter = ['customer_type', 'is_active', 'city']
    search_fields = ['customer_number', 'name', 'company_name', 'email', 'phone']
    readonly_fields = ['customer_number', 'created_at', 'updated_at']
    inlines = [ContactInline]
    
    fieldsets = (
        ('פרטי לקוח', {
            'fields': ('customer_number', 'customer_type', 'is_active')
        }),
        ('פרטים אישיים', {
            'fields': ('name', 'id_number'),
            'classes': ('collapse',),
        }),
        ('פרטי חברה', {
            'fields': ('company_name', 'business_number'),
            'classes': ('collapse',),
        }),
        ('התקשרות', {
            'fields': ('email', 'phone', 'mobile')
        }),
        ('כתובת', {
            'fields': ('street', 'city', 'postal_code', 'country')
        }),
        ('נוסף', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_inline_instances(self, request, obj=None):
        """מציג inline רק עבור לקוחות קיימים"""
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(Installer)
class InstallerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'city', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['company_name', 'email', 'phone']
    inlines = [ContactInline]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier_type', 'phone', 'is_active']
    list_filter = ['supplier_type', 'is_active']
    search_fields = ['name', 'email']
    inlines = [ContactInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'entity_type', 'related_entity', 'role', 'phone', 'email', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    
    def entity_type(self, obj):
        return obj.entity_type
    entity_type.short_description = 'סוג ישות'
