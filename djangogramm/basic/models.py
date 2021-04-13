import os

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from time import gmtime, strftime

from stdimage import StdImageField
from autoslug import AutoSlugField


class GrammUserManager(BaseUserManager):
    """Сustomized user manager"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class GrammUser(AbstractUser):
    """Custom User model without username"""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = GrammUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """User profile"""

    def user_directory_path(instance, filename):
        return os.path.join(
            'profiles',
            ' '.join([str(instance.first_name), str(instance.last_name)]),
            'avatar',
            filename
        )

    def get_slug(instance):
        pass

    gramm_user = models.OneToOneField(GrammUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    bio = models.TextField(max_length=1023, blank=True, default='', verbose_name=_("Biography"))
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    identifier = models.CharField(max_length=128, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'profile_identifier': self.identifier})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Save profile.identifier as slug:identifier from profile.first_name and profile.last_name"""

        if not self.identifier:
            self.identifier = slugify(f"{self.first_name} {self.last_name}")
        return super(Profile, self).save()


class Post(models.Model):
    """User's post"""

    def get_slug(instance):
        return slugify(f"{instance.profile} {instance.title}")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Profile'))
    title = models.CharField(max_length=64, verbose_name=_("Post title"))
    time_create = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=get_slug, unique=True, db_index=True)

    class Meta:
        ordering = ['profile', 'time_create']

    def __str__(self):
        return f"{self.profile} - {self.title}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'profile_identifier': self.profile, 'post_slug': self.slug})


class Photo(models.Model):
    """User's photo"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)

    def user_directory_path(instance, filename):
        return os.path.join(
            'profiles',
            ' '.join([str(instance.post.profile.first_name), str(instance.post.profile.last_name)]),
            'post-photos',
            strftime(os.path.join('%Y', '%B', '%d'), gmtime()),
            '-'.join(slugify(instance.post.title).split('-')[:3]),
            filename
        )

    photo = StdImageField(upload_to=user_directory_path, delete_orphans=True, variations={'thumbnail': (250, 250)})

    def __str__(self):
        return f"{self.post} - {self.pk}"

    def get_absolute_url(self):
        pass
