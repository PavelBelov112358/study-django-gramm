from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst
from django.contrib.auth import (
    authenticate, get_user_model
)

from .models import Profile, Post, Photo


UserModel = get_user_model()


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'identifier', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'style': 'resize:none;'}),
        }


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'identifier', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'style': 'resize:none;'}),
        }


class CreatePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(CreatePostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title',)
        widgets = {
            'title': forms.Textarea(attrs={'cols': 70, 'rows': 1, 'style': 'resize:none;'}),
        }

    photos = forms.ImageField(label=_("Photos"), widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_photos(self):
        photos = self.files.getlist('photos')
        if len(photos) > 10:
            raise ValidationError("The number of photos in a post is limited to 10")
        return photos

    def save(self, commit=True):
        post = super(CreatePostForm, self).save(commit=False)
        post.profile = self.profile
        if commit:
            post.save()
            [Photo.objects.create(photo=photo, post=post) for photo in self.files.getlist('photos')]
        return post


class AuthenticationEmailForm(forms.Form):
    """
    Customized class for authenticating users. This form accepts email/password logins.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "email" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['email'].max_length = username_max_length
        self.fields['email'].widget.attrs['maxlength'] = username_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )
