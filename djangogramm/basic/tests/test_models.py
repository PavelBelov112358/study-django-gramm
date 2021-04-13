import os
import urllib

import pytest
from django.conf import settings
from mixer.backend.django import mixer

from basic.models import GrammUser, Profile, Post, Photo


@pytest.fixture
def grammuser(db):
    yield mixer.blend(GrammUser)


@pytest.fixture
def profile(db):
    yield mixer.blend(Profile)


@pytest.fixture
def post(db):
    return mixer.blend(Post)


@pytest.fixture
def photo(db):
    photo = mixer.blend(Photo)

    yield photo

    photo_url = urllib.parse.unquote(photo.photo.url)
    folder_url = '\\'.join(photo_url.split('/')[2:-1])

    photo.delete()
    os.removedirs(os.path.abspath(f'{settings.MEDIA_ROOT}\\{folder_url}'))


def test_grammuser_model(grammuser):
    assert grammuser.__class__ is GrammUser
    assert str(grammuser) == grammuser.email


def test_profile_model(profile):
    assert profile.__class__ is Profile
    assert str(profile) == f"{profile.first_name} {profile.last_name}"


def test_post_model(post):
    assert post.__class__ is Post
    assert str(post) == f"{post.profile} - {post.title}"


def test_photo_model(photo):
    assert photo.__class__ is Photo
    assert str(photo) == f"{photo.post} - {photo.pk}"
