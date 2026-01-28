from django.db import models

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
