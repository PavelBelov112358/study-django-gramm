from django.urls import reverse, resolve


def test_registration_url():
    url_name = 'django-registration-register'
    try:
        path = reverse(url_name)
    except:
        assert False, f'Path "{url_name}" not found'
