# adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # if the user is logged in and they try to add a social account
        if request.user.is_authenticated:
            return redirect('/menu_f/')
        # if not authenticated, check if the email is already in use
        email = sociallogin.account.extra_data.get('email', '').lower()
        if email:
            try:
                # Try to find an existing user with this email address
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass  # Proceed with normal signup flow
