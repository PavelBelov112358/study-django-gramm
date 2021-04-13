from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationUserForm(UserCreationForm):
    """ Form for registering a new user account. """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'email',
            "password1",
            "password2",
        ]