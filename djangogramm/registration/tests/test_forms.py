import pytest

from django.conf import settings

from model_bakery import baker

from registration.forms import RegistrationUserForm


@pytest.mark.django_db
def test_registration_user_form():
    user = baker.prepare(settings.AUTH_USER_MODEL)
    valid_form_data = {
        'email': user.email,
        'password1': user.password,
        'password2': user.password,
    }
    form = RegistrationUserForm(data=valid_form_data)

    assert form.is_valid()
    assert not form.errors


@pytest.mark.django_db
def test_registration_user_form_invalid():
    invalid_form_data = {
        'email': 'test',
        'password1': 'test',
        'password2': 'test',
    }
    form = RegistrationUserForm(data=invalid_form_data)

    assert not form.is_valid()
    assert form.errors.get('email') == ['Enter a valid email address.']
    assert form.errors.get('password2') == \
           ['This password is too short. It must contain at least 8 characters.', 'This password is too common.']
