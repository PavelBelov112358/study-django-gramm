from django.shortcuts import redirect
from django.urls import reverse

from .models import Profile

menu = [
    {"title": "MyProfile", "url_name": "my-profile"},
    {"title": "New post", "url_name": "new-post"},
    {"title": "People", "url_name": "people"},
    {"title": "Log out", "url_name": "logout"},
]


class ContextDataMixin:
    """Add context"""

    def get_context(self, **kwargs):
        """Add menu and transmitted kwargs to the context"""

        context = kwargs
        context["menu"] = menu
        return context


class SuccessReverseProfileMixin:
    """Override get_success_url() method in order to redirect user profile"""

    def get_success_url(self):
        """Redirect to profile with property identifier"""

        if not Profile.objects.filter(gramm_user=self.request.user).exists():
            return reverse("new-profile")
        return reverse(
            "user-profile",
            kwargs={"profile_identifier": self.request.user.profile.identifier}
        )
