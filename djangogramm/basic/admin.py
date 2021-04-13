from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import *


@admin.register(GrammUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom GrammUser model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('email',)
    search_fields = ('email',)
    ordering = ('email',)
    list_editable = ('is_active', 'is_staff', 'is_superuser')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('gramm_user', 'first_name', 'last_name', 'bio', 'get_html_avatar')
    ordering = ('gramm_user',)

    fields = ('gramm_user', 'first_name', 'last_name', 'bio', 'avatar', 'get_html_avatar')
    readonly_fields = ('get_html_avatar',)

    def get_html_avatar(self, object):
        if object.avatar:
            return mark_safe(f"<img src='{object.avatar.url}' width=100>")
        else:
            return mark_safe(f"{_('No photo')}")

    get_html_avatar.short_description = "Avatar"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'time_create')
    search_fields = ('title', 'profile')
    list_filter = ('profile',)
    ordering = ('profile', 'time_create')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post', 'time_create', 'get_html_photo')

    fields = ('post', 'photo', 'get_html_photo')
    readonly_fields = ('get_html_photo',)
    list_filter = ('post',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100>")
        else:
            return _("No photo")

    get_html_photo.short_description = "Photo"
