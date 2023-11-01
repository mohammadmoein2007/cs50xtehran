# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import secrets
import string
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Additional custom fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Many-to-many relationship with groups and permissions
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='user permissions', blank=True, related_name='custom_users'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=100)
    latin = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.latin)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(self.id)
            self.save()
    
class Tag(models.Model):
    title = models.CharField(max_length=100)
    latin = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.latin)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(self.id)
            self.save()
    
class Article(models.Model):
    title = models.CharField(max_length=300)
    latin = models.CharField(max_length=300)
    article = models.TextField()
    cover = models.ImageField(upload_to="covers/")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.latin)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(self.id)
            self.save()

class City(models.Model):
    name = models.CharField(max_length=100)
    latin = models.CharField(max_length=300)
    cover = models.ImageField(upload_to='cities/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.latin)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(self.id)
            self.save()

class Travelogue(models.Model):
    title = models.CharField(max_length=300)
    latin = models.CharField(max_length=300)
    content = models.TextField()
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
            return self.title

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.slug:
            now = datetime.now()
            self.slug = slugify(self.latin)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(self.id)
            self.save()

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(CustomUser, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for i in range(40))


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)