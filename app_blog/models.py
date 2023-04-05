from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_size(value):
    filesize = value.size
    if filesize > 5*1024*1024:
        raise ValidationError(
            _("The maximum file size that can be uploaded is 5MB.")
        )



class BlogQuerySet(models.QuerySet):
    def is_deleted(self):
        return self.filter(is_deleted=False)

    def search(self, query, is_draft=None):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_deleted()
        if is_draft is not None:
            qs = qs.filter(published=not is_draft)
        qs = qs.filter(lookup)
        return qs




class BlogManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)




class Blog(models.Model):
    title = models.CharField(unique=True, max_length=550, null=False)
    slug = models.SlugField(unique=True, max_length=255, null=False)
    image = models.ImageField(null=False, validators=[validate_image_size])
    description = models.TextField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)

    objects = BlogManager()

    def save(self, *args, **kwargs):
        if self.published and not self.date_published:
            self.date_published = timezone.now()
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
        ordering = ['-date_published', '-date_updated', '-date_created']

    def __str__(self):
        return self.title