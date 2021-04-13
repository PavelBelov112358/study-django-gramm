import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict

from model_bakery import baker

from basic.forms import CreateProfileForm, UpdateProfileForm, CreatePostForm
from basic.models import Profile


@pytest.mark.django_db
def test_create_profile_form():
    profile = baker.prepare(Profile)
    valid_form_data = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'identifier': f'{profile.first_name[:5]}-{profile.last_name[:5]}',
        'bio': profile.bio,
        'avatar': profile.avatar,
    }
    form = CreateProfileForm(data=valid_form_data)

    assert form.is_valid()
    assert not form.errors


@pytest.mark.django_db
def test_create_profile_form_empty():
    empty_form_data = {}
    form = CreateProfileForm(data=empty_form_data)

    assert not form.is_valid()

    assert form.errors.get('first_name') == ['This field is required.']
    assert form.errors.get('last_name') == ['This field is required.']
    assert form.errors.get('identifier') == ['This field is required.']


@pytest.mark.django_db
def test_update_profile_form():
    profile = baker.prepare(Profile)
    valid_form_data = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'identifier': f'{profile.first_name[:5]}-{profile.last_name[:5]}',
        'bio': profile.bio,
        'avatar': profile.avatar,
    }
    form = UpdateProfileForm(data=valid_form_data)

    assert form.is_valid()
    assert not form.errors


@pytest.mark.django_db
def test_update_profile_form_empty():
    empty_form_data = {}
    form = UpdateProfileForm(data=empty_form_data)

    assert not form.is_valid()

    assert form.errors.get('first_name') == ['This field is required.']
    assert form.errors.get('last_name') == ['This field is required.']
    assert form.errors.get('identifier') == ['This field is required.']


@pytest.mark.django_db
def test_create_post_form():
    profile = baker.prepare(Profile)
    valid_form_data = {'title': 'test post'}
    img = SimpleUploadedFile('test.png', b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                                         b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02')
    valid_form_files = QueryDict(mutable=True)
    valid_form_files.update({'photos': img})
    form = CreatePostForm(valid_form_data, valid_form_files, profile=profile)

    assert form.is_valid()
    assert not form.errors



@pytest.mark.django_db
def test_create_post_form_empty():
    profile = baker.prepare(Profile)
    empty_form_data = {}
    empty_form_files = {}
    form = CreatePostForm(empty_form_data, empty_form_files, profile=profile)

    assert not form.is_valid()

    assert form.errors.get('title') == ['This field is required.']
    assert form.errors.get('photos') == ['This field is required.']


@pytest.mark.django_db
def test_create_post_form_too_many_photos():
    profile = baker.prepare(Profile)
    valid_form_data = {'title': 'test post'}
    img = SimpleUploadedFile('test.png', b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                                         b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02')

    invalid_form_files = QueryDict(mutable=True)
    [invalid_form_files.update({'photos': img}) for _ in range(11)]
    form = CreatePostForm(valid_form_data, invalid_form_files, profile=profile)

    assert not form.is_valid()
    assert form.errors.get('photos') == ['The number of photos in a post is limited to 10']
