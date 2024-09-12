from django.db import models
from django.urls import reverse
from common.authentication import get_user_data


class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def save(self, *args, **kwargs):
        user = get_user_data()
        if not self.created_by and user:
            self.created_by = user.user_id
        if not self.pk:
            self.updated_by = user.user_id
        super().save(*args, **kwargs)
