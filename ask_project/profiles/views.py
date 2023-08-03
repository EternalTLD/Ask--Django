from typing import Any, Dict
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView

from .forms import UserEditForm, ProfileEditForm
from users.models import User
from questions.models import Question

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DetailView, self).get_context_data(**kwargs)
        user_questions = self.get_user_questions()
        context['user_questions'] = user_questions
        context['page_obj'] = user_questions
        return context
    
    def get_user_questions(self):
        user = self.get_object()
        user_questions = Question.objects.filter(author=user)
        paginator = Paginator(user_questions, 3)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        return page_obj


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
