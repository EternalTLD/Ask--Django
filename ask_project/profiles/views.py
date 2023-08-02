from django.shortcuts import render

from .forms import UserEditForm, ProfileEditForm


def profile_edit_view(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                  data=request.POST, 
                                  files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'profiles/profile_edit_form.html', context={'user_form': user_form, 
                                                                       'profile_form': profile_form})
