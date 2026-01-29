from django.db import models
from django.conf import settings
from core.models import ActiveModel, AddressMixin
from core.constants import LeadStatus, ContractType, ContractStatus, LeadSource
from core.validators import phone_validator
from core.utils import generate_unique_number


class Lead(ActiveModel, AddressMixin):
    """
    Lead - Potential customer. initial contact
    """
    lead_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name = 'מספר ליד'
    )
    lead_source = models.CharField(
        choices=LeadSource.choices,
        verbose_name = 'מקור ליד',
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default= LeadStatus.NEW,
        verbose_name = 'סטטוס'
    )

    # Contact Information
    contact_name = models.CharField(max_length=200, verbose_name='שם איש קשר')
    email = models.EmailField(blank=True, verbose_name='אימייל')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name='טלפון'
    )

    # Requirement Information
    estimated_system_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='גודל מערכת משוער (kWp)'
    )

    # Assignment and Relations
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null=True,
        blank = True,
        related_name= 'assigned_leads',
        verbose_name = 'בעלים'
    )
    customer = models.ForeignKey(
        'crm.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='לקוח (לאחר המרה)'
    )
    notes = models.TextField(blank=True, verbose_name='הערות')

    class Meta:
        verbose_name = 'ליד'
        verbose_name_plural = 'לידים'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.lead_number} | {self.contact_name}'

    def save(self, *args, **kwargs):
        if not self.lead_number:
            self.lead_number = generate_unique_number('LED', Lead, 'lead_number')
        super().save(*args, **kwargs)


    def convert_to_customer(self):
        """
        converting a lead to customer and contact
        """
        from crm.models import Customer, Contact
        from core.constants import CustomerType
        
        if self.customer:
            return self.customer
        
        # יצירת לקוח
        customer = Customer.objects.create(
            name=self.contact_name,
            email=self.email,
            phone=self.phone,
            street=self.street,
            city=self.city,
            postal_code=self.postal_code,
            country=self.country,
        )
        
        # יצירת איש קשר
        name_parts = self.contact_name.split(maxsplit=1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        Contact.objects.create(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            email=self.email,
            phone=self.phone,
            is_primary=True,
        )
        
        # עדכון הליד
        self.customer = customer
        self.status = LeadStatus.WON
        self.save()
        
        return customer


class Contract(ActiveModel):
    """
    contract made with a potential customer or lead
    """
    contract_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name='מספר חוזה'
    )
    contract_type = models.CharField(
        max_length=20,
        choices=ContractType.choices,
        verbose_name='סוג חוזה'
    )
    status = models.CharField(
        max_length=20,
        choices=ContractStatus.choices,
        default=ContractStatus.DRAFT,
        verbose_name='סטטוס'
    )

    # Relations
    customer = models.ForeignKey(
        'crm.Customer',
        on_delete=models.PROTECT,
        related_name='contracts',
        verbose_name='לקוח'
    )

    # Contract Conditions
    start_date = models.DateField(verbose_name='תאריך התחלה')
    end_date = models.DateField(null=True, blank=True, verbose_name='תאריך סיום')
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='שווי החוזה'
    )
    payment_terms = models.TextField(blank=True, verbose_name='תנאי תשלום')

    # Files
    document = models.FileField(
        upload_to='contracts/',
        blank=True,
        verbose_name='מסמך חוזה'
    )

    notes = models.TextField(blank=True, verbose_name='הערות')

    class Meta:
        verbose_name = 'חוזה'
        verbose_name_plural = 'חוזים'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.contract_number} | {self.customer}'

    def save(self, *args, **kwargs):
        if not self.contract_number:
            self.contract_number = generate_unique_number('CON', Contract, 'contract_number')
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if not self.end_date:
            return False
        from django.utils import timezone
        return self.end_date < timezone.now().date()

    @property
    def duration_days(self):
        if not self.end_date:
            return None
        return (self.end_date - self.start_date).days