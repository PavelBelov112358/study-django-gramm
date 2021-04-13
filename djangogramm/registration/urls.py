from django.urls import path, include

from .views import RegistrationUserView

urlpatterns = [
    path('register/', RegistrationUserView.as_view(), name='django-registration-register'),

    # Activation uses path 'activate/*'
    path('', include('django_registration.backends.activation.urls')),
]
