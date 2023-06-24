from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import FileExtensionValidator

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(default='profile/avatar.svg', upload_to='profile/', null=True,
                               validators=[FileExtensionValidator(['jpg', 'svg', 'png'])])
    social_twitter = models.URLField(max_length=500, blank=True, null=True)
    social_linkedin = models.URLField(max_length=500, blank=True, null=True)
    social_facebook = models.URLField(max_length=500, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
