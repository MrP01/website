from django.conf.urls.defaults import *

from userena import views as userena_views

from . import forms

urlpatterns = patterns('',
    url(r'^signin/$',
        userena_views.signin,
        {'auth_form': forms.AuthenticationForm},
        name='userena_signin'),
    url(r'^signup/$',
        userena_views.signup,
        {'signup_form': forms.SignupForm},
        name='userena_signup'),
    url(r'^(?P<username>[\.\w]+)/email/$',
        userena_views.email_change,
        {'email_form': forms.ChangeEmailForm},
        name='userena_email_change'),
    url(r'^(?P<username>[\.\w]+)/password/$',
        userena_views.password_change,
        {'pass_form': forms.PasswordChangeForm},
        name='userena_password_change'),
    url(r'^(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {'edit_profile_form': forms.EditProfileForm},
        name='userena_profile_edit'),
)