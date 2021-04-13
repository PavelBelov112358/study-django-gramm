from django.conf import settings
from django.test import TestCase, override_settings, Client
from django.urls import reverse

import lxml.html as html
from mixer.backend.django import mixer

from basic.models import Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestHomeView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.path = reverse('home')

    def test_home_unauthenticated(self):
        expected_form_fields = [
            'email',
            'password',
        ]
        response = self.client.get(self.path)
        form = html.fromstring(response.content).forms[0]

        assert response.status_code == 200
        assert form.fields.get('csrfmiddlewaretoken')
        assert expected_form_fields == form.fields.keys()[1:]

    def test_home_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert response.url == reverse('my-profile')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestUserProfileView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.path = reverse('my-profile')

    def test_user_unauthenticated(self):
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert self.path in response.url

    def test_user_without_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert response.url == reverse('new-profile')

    def test_user_with_profile(self):
        profile = mixer.blend(Profile, gramm_user=self.user)
        client = Client()
        client.force_login(self.user)
        response = client.get(self.path)
        content = response.content.decode()

        assert response.status_code == 200
        assert profile.first_name in content
        assert profile.last_name in content

    def test_user_redirect_profile(self):
        profile = mixer.blend(Profile, gramm_user=self.user)
        self.client.force_login(self.user)
        path = reverse('user-profile', kwargs={'profile_identifier': profile.identifier})
        response = self.client.get(path)

        assert response.status_code == 302
        assert response.url == self.path

    def test_user_someone_profile(self):
        profile = mixer.blend(Profile, gramm_user=self.user)
        smn_profile = mixer.blend(Profile)
        self.client.force_login(self.user)
        path = reverse('user-profile', kwargs={'profile_identifier': smn_profile.identifier})
        response = self.client.get(path)
        content = response.content.decode()

        assert response.status_code == 200
        assert smn_profile.first_name in content
        assert smn_profile.last_name in content


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestCreateProfileView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.path = reverse('new-profile')

    def test_user_unauthenticated(self):
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert self.path in response.url

    def test_create_profile_view(self):
        expected_form_fields = [
            'first_name',
            'last_name',
            'identifier',
            'bio',
            'avatar',
        ]

        self.client.force_login(self.user)
        response = self.client.get(self.path)
        form = html.fromstring(response.content).forms[0]

        assert response.status_code == 200
        assert form.fields.get('csrfmiddlewaretoken')
        assert expected_form_fields == form.fields.keys()[1:]


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestUpdateProfileView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.profile = mixer.blend(Profile, gramm_user=self.user)
        self.path = reverse('settings-profile', kwargs={'profile_identifier': self.profile.identifier})

    def test_user_unauthenticated(self):
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert self.path in response.url

    def test_update_profile_view(self):
        expected_form_fields = [
            'first_name',
            'last_name',
            'identifier',
            'bio',
            'avatar',
        ]

        self.client.force_login(self.user)
        response = self.client.get(self.path)
        form = html.fromstring(response.content).forms[0]

        assert response.status_code == 200
        assert form.fields.get('csrfmiddlewaretoken')
        assert expected_form_fields == form.fields.keys()[1:]


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestPeopleView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.path = reverse('people')

    def test_user_unauthenticated(self):
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert self.path in response.url

    def test_people_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        assert response.status_code == 200
        assert b'People' in response.content


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestCreatePostView(TestCase):

    def setUp(self) -> None:
        self.user = mixer.blend(settings.AUTH_USER_MODEL)
        self.profile = mixer.blend(Profile, gramm_user=self.user)
        self.path = reverse('new-post')

    def test_user_unauthenticated(self):
        response = self.client.get(self.path)

        assert response.status_code == 302
        assert self.path in response.url

    def test_create_post_view(self):
        expected_form_fields = [
            'title',
            'photos',
        ]

        self.client.force_login(self.user)
        response = self.client.get(self.path)
        form = html.fromstring(response.content).forms[0]

        assert response.status_code == 200
        assert form.fields.get('csrfmiddlewaretoken')
        assert expected_form_fields == form.fields.keys()[1:]
