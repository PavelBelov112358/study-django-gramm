from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from .forms import CreateProfileForm, UpdateProfileForm, CreatePostForm, AuthenticationEmailForm
from .models import Profile, Photo, Post
from .utils import SuccessReverseProfileMixin, ContextDataMixin


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found (404)</h1>")


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


class HomeView(SuccessReverseProfileMixin, LoginView):
    form_class = AuthenticationEmailForm
    template_name = 'basic/home.html'
    extra_context = dict(title='DjangoGramm')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return redirect('my-profile')
        return super(HomeView, self).get(request, *args, **kwargs)
    
    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse('people')
        return super(HomeView, self).get_success_url()


class CreateProfileView(LoginRequiredMixin, SuccessReverseProfileMixin, CreateView):
    form_class = CreateProfileForm
    template_name = "basic/profile_form.html"
    extra_context = dict(title='New profile',
                         heading='Create your profile')

    def form_valid(self, form):
        """Add user to form"""

        obj = form.save(commit=False)
        obj.gramm_user = self.request.user
        obj.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, ContextDataMixin, SuccessReverseProfileMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "basic/profile_form.html"
    slug_url_kwarg = "profile_identifier"
    slug_field = 'identifier'

    def get(self, request, *args, **kwargs):
        """Check if the profile belongs to the user"""

        if not self.request.user.profile == self.get_object():
            raise Http404
        return super(UpdateProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        extra_context = self.get_context(title='Profile settings',
                                         heading='Profile settings')
        return {**context, **extra_context}


class UserProfileView(LoginRequiredMixin, ContextDataMixin, DetailView):
    model = Profile
    template_name = 'basic/profile.html'
    slug_url_kwarg = 'profile_identifier'
    slug_field = 'identifier'

    def get_object(self, queryset=None):
        """If the user is redirected to the URL "my-profile",URL doesn't require "slug:profile_identifier" """

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        if self.request.path == reverse_lazy('my-profile'):
            pk = self.request.user.id
        slug = self.kwargs.get(self.slug_url_kwarg)

        if pk is not None:
            queryset = queryset.filter(gramm_user_id=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()

        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get(self, request, *args, **kwargs):
        """If the authorized user goes to his own profile, he'll be redirected to the URL "my-profile" """

        if self.request.user.is_staff:
            return super(UserProfileView, self).get(request, *args, **kwargs)

        if not Profile.objects.filter(gramm_user=self.request.user).exists():
            return redirect('new-profile')

        if self.kwargs.get(self.slug_url_kwarg) == Profile.objects.get(gramm_user=self.request.user).identifier:
            return redirect('my-profile')

        return super(UserProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}

        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object

            context['posts'] = list(map(
                lambda post:
                Photo.objects.filter(post=post),
                Post.objects.filter(profile=self.object.id).order_by('-time_create')
            ))

            context['title'] = f"DjangoGramm - {self.object}"

            context["is_owner"] = (self.request.user == self.object.gramm_user)

        context.update(kwargs)
        context.update(self.get_context())

        return super().get_context_data(**context)


class PeopleView(LoginRequiredMixin, ContextDataMixin, ListView):
    model = Profile
    template_name = "basic/people.html"
    context_object_name = "people"
    
    def get_queryset(self):
        """Return queryset without authorized user"""
        return super(PeopleView, self).get_queryset().exclude(gramm_user=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        extra_context = self.get_context(title='People')
        return {**context, **extra_context}


class CreatePostView(LoginRequiredMixin, SuccessReverseProfileMixin, ContextDataMixin, CreateView):
    form_class = CreatePostForm
    template_name = "basic/post_form.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        extra_context = self.get_context(title='New post')
        return {**context, **extra_context}
    
    def get_form_kwargs(self):
        """Passes the request object for instantiating the form.

        It's necessary to assign created post to current user"""

        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs['profile'] = self.request.user.profile
        return kwargs
