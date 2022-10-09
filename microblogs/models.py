from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(max_length=30,unique = True, 
    validators=[RegexValidator(
        regex = r'^@\w{3,}$',
        message = 'Username must consist of @ followed by at least three alphanumericals'
    )])

    bio = models.TextField()