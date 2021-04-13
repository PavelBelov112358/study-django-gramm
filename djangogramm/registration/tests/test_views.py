from django.test import TestCase
from django.urls import reverse

import lxml.html as html


class TestRegistrationUserView(TestCase):

    def test_registration_user_view(self):
        expected_form_fields = [
            'email',
            'password1',
            'password2',
        ]

        path = reverse('django-registration-register')
        response = self.client.get(path)
        form = html.fromstring(response.content).forms[0]

        assert response.status_code == 200
        assert form.fields.get('csrfmiddlewaretoken')
        assert expected_form_fields == form.fields.keys()[1:]
