from django.urls import reverse, resolve


def test_home_url():
    url_name = 'home'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'


def test_logout_url():
    url_name = 'logout'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'


def test_my_profile_url():
    url_name = 'my-profile'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'


def test_user_profile_url():
    url_name = 'user-profile'
    try:
        path = reverse(url_name, kwargs={'profile_identifier': 'identifier'})
    except:
        assert False, f'Path "{url_name}" not found'


def test_new_profile_url():
    url_name = 'new-profile'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'


def test_settings_profile_url():
    url_name = 'settings-profile'
    try:
        path = reverse(url_name, kwargs={'profile_identifier': 'test'})
    except:
        assert False, f'Path "{url_name}" not found'


def test_people_url():
    url_name = 'people'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'


def test_new_post_url():
    url_name = 'new-post'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'
