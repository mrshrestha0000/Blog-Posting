from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # published_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
            
    #     return super().save(*args, **kwargs)
            
# def slugify_instance_title(instance, save=False):
#     slug = slugify(instance.title)
#     qs = Article.objects.filter(slug=slug).exclude(id=instance.id)
#     if qs.exists():
#         slug = f"{slug}-{qs.count()+1}"
#     instance.slug = slug
#     if save:
#         instance.save()
#     return instance
            
# def article_pre_save(sender, instance, *args, **kwargs):
#     print('pre_save')
#     if instance.slug is None:
#         slugify_instance_title(instance, save=False)

# pre_save.connect(article_pre_save, sender=Article)

# def article_post_save(sender, instance, created, *args, **kwargs):
#     print('post_save')
#     if created:
#         slugify_instance_title(instance, save=True)
#     print(*args, **kwargs)

# post_save.connect(article_post_save, sender=Article)
        
