from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.utils.text import slugify


class BlogQuerySet(models.QuerySet):
    def is_deleted(self):
        return self.filter(is_deleted=False)

    def search(self, query):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_deleted().filter(lookup)
        return qs


class BlogManager(models.QuerySet):
    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self.db)

    def search(self, query):
        return self.get_queryset().search(query)


class Blog(models.Model):

    title = models.CharField(unique=True, max_length=550, null=False)
    slug = models.SlugField(unique=True, max_length=255, null=False)
    image = models.ImageField(null=True)
    description = models.TextField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    objects = BlogManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, hard=False):
        if not self.is_deleted:
            self.is_deleted = True
            self.date_deleted = timezone.now()
            self.save(update_fields=['is_deleted', 'date_deleted'])
        elif hard:
            super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.date_deleted = None
            self.save(update_fields=['is_deleted', 'date_deleted'])

    class Meta:
        ordering = ['-date_updated', '-date_created']

    def __str__(self):
        return self.title

