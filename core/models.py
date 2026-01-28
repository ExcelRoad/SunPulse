from django.db import models
from django_countries.fields import CountryField

class BaseModel(models.Model):

    '''
    Base model for all models to use
    '''

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class ActiveManager(models.Manager):

    '''
    Manager that returns only active records
    '''

    def get_queryset(self):
        return super().get_queryset().filter(is_active = True)


class ActiveModel(BaseModel):

    '''
    Base model with support of soft delete
    '''

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])


class AddressMixin(models.Model):
    """
    Mixin for address fields - to use for all models with address
    """
    street = models.CharField(max_length=200, blank=True, verbose_name='רחוב')
    city = models.CharField(max_length=100, blank=True, verbose_name='עיר')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='מיקוד')
    country = CountryField(default='IL', verbose_name='מדינה')

    class Meta:
        abstract = True

    @property
    def full_address(self):
        parts = [self.street, self.city, self.postal_code, str(self.country.name)]
        return ', '.join(p for p in parts if p)
