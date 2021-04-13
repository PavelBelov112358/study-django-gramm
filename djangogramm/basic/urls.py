from django.urls import path
from .views import logout_user, UserProfileView, HomeView, UpdateProfileView, CreateProfileView, PeopleView, \
    CreatePostView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('logout/', logout_user, name='logout'),

    path('profile/me/', UserProfileView.as_view(), name='my-profile'),
    path('profile/<slug:profile_identifier>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/new', CreateProfileView.as_view(), name="new-profile"),
    path('profile/<slug:profile_identifier>/settings/', UpdateProfileView.as_view(), name='settings-profile'),

    path('people/', PeopleView.as_view(), name='people'),

    path('post/new/', CreatePostView.as_view(), name='new-post'),
]
