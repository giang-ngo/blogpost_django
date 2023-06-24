from django.db import models
from users.models import User
import uuid
from django.core.validators import FileExtensionValidator

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    featured_image = models.ImageField(
        default='blog/default.jpg', upload_to='blog/', null=True,
        validators=[FileExtensionValidator(['jpg', 'svg', 'png'])])
    description = models.TextField(blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.title

    @property
    def imageURL(self):
        try:
            img = self.featured_image.url
        except:
            img = ''
        return img


class Message(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey(
        'self', related_name='parent_comment', on_delete=models.CASCADE,
        null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.body


class Topic(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name
