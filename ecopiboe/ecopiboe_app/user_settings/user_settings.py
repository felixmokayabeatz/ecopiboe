from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from ecopiboe_app.forms import UserProfileForm, CustomPasswordChangeForm

@login_required(login_url='/login/')
def user_settings(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')
        else:
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        user_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'users/user_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })
