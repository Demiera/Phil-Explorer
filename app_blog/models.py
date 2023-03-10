from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(unique=True, max_length=550, null=False)
    image = models.ImageField(null=True)
    description = models.TextField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        if not self.is_deleted:
            self.is_deleted = True
            self.date_deleted = timezone.now()
            self.save(update_fields=['is_deleted', 'date_deleted'])

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.date_deleted = None
            self.save(update_fields=['is_deleted', 'date_deleted'])


    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

