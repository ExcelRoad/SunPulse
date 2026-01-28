from django.db import models
from core.models import ActiveModel, AddressMixin
from core.constants import CustomerType, SupplierType
from core.validators import phone_validator, israeli_id_validator
from core.utils import generate_unique_number


class Customer(ActiveModel, AddressMixin):
    """
    Customer can be private or business (installer)
    """

    customer_number = models.CharField(
        max_length= 20,
        unique= True,
        editable=False,
        verbose_name = 'מספר לקוח'
    )
    customer_type = models.CharField(
        max_length=20,
        choices=CustomerType.choices,
        default = CustomerType.PRIVATE,
        verbose_name = 'סוג לקוח'
    )

    # Contact Info for private customer
    first_name = models.CharField(max_length=100, blank=True, verbose_name='שם פרטי')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='שם משפחה')
    id_number = models.CharField(max_length=9, blank=True,validators=[israeli_id_validator], verbose_name='תעודת זהות')

    # Info for business customer
    company_name = models.CharField(max_length=200, blank=True, verbose_name='חברה')
    business_number = models.CharField(max_length=20, blank=True, verbose_name='ח.פ')

    # Contact Info
    email = models.EmailField(blank=True, verbose_name='אימייל')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name = 'טלפון'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name = 'נייד'
    )

    notes = models.TextField(blank=True, verbose_name='הערות')

    class Meta:
        verbose_name = 'לקוח'
        verbose_name_plural = 'לקוחות'
        ordering = ['-created_at']

    def __str__(self):
        if self.customer_type == CustomerType.BUSINESS:
            return f'{self.customer_number} | {self.company_bane}'
        return f'{self.customer_number} | {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """ Adding customer number on save """
        if not self.customer_number:
            self.customer_number = generate_unique_number('CUS', Customer, 'customer_number')
        super().save(*args, **kwargs)


    @property
    def display_name(self):
        if self.customer_type == CustomerType.BUSINESS:
            return self.company_name
        return f'{self.first_name} {self.last_name}'.strip()



class Installer(ActiveModel, AddressMixin):
    """
    Installing company or person
    """
    company_name = models.CharField(max_length=200, verbose_name='שם החברה')
    email = models.EmailField(blank=True, verbose_name='אימייל')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name='טלפון'
    )

    license_number = models.CharField(max_length=50, blank=True, verbose_name='מספר רישיון')
    notes = models.TextField(blank=True, verbose_name='הערות')

    class Meta:
        verbose_name = 'מתקין'
        verbose_name_plural = 'מתקינים'
        ordering = ['company_name']

    def __str__(self):
        return self.company_name



class Supplier(ActiveModel, AddressMixin):
    """
    Supplier of services or goods
    """
    name = models.CharField(max_length=200, verbose_name='שם הספק')
    supplier_type = models.CharField(
        max_length=20,
        choices=SupplierType.choices,
        default=SupplierType.EQUIPMENT,
        verbose_name='סוג ספק'
    )
    email = models.EmailField(blank=True, verbose_name='אימייל')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name='טלפון'
    )

    notes = models.TextField(blank=True, verbose_name='הערות')

    class Meta:
        verbose_name = 'ספק'
        verbose_name_plural = 'ספקים'
        ordering = ['name']

    def __str__(self):
        return self.name



class Contact(ActiveModel):
    """
    A contact can be related to customer, supplier or installer.
    """
    # Relations
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name='לקוח'
    )
    installer = models.ForeignKey(
        Installer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name='מתקין'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name='ספק'
    )
    
    # פרטי איש הקשר
    name = models.CharField(max_length=200, verbose_name='שם')
    role = models.CharField(max_length=100, blank=True, verbose_name='תפקיד')
    email = models.EmailField(blank=True, verbose_name='אימייל')
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        verbose_name='טלפון'
    )
    is_primary = models.BooleanField(default=False, verbose_name='איש קשר ראשי')

    class Meta:
        verbose_name = 'איש קשר'
        verbose_name_plural = 'אנשי קשר'
        ordering = ['-is_primary', 'name']

    def __str__(self):
        return f'{self.name} ({self.related_entity})'

    def clean(self):
        """ Make sure only one relation is active """
        from django.core.exceptions import ValidationError
        
        relations = [self.customer, self.installer, self.supplier]
        filled = [r for r in relations if r is not None]
        
        if len(filled) == 0:
            raise ValidationError('חובה לשייך את איש הקשר ללקוח, מתקין או ספק')
        if len(filled) > 1:
            raise ValidationError('איש קשר יכול להיות משויך רק לישות אחת')

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # If this record is the primary, remove primary from other records with the same relation
        if self.is_primary:
            Contact.objects.filter(
                customer=self.customer,
                installer=self.installer,
                supplier=self.supplier,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        
        super().save(*args, **kwargs)

    @property
    def related_entity(self):
        """ Return the related object """
        return self.customer or self.installer or self.supplier

    @property
    def entity_type(self):
        """ Return the related object model name """
        if self.customer:
            return 'customer'
        if self.installer:
            return 'installer'
        if self.supplier:
            return 'supplier'
        return None



