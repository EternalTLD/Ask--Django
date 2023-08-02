from django.shortcuts import render
from django.views.generic.detail import DetailView

from .forms import UserEditForm, ProfileEditForm
from users.models import User

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

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
