from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import UserEditForm, ProfileEditForm
from users.models import User
from questions.models import Question

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile_detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.model.objects.select_related('profile').prefetch_related('questions').get(username=self.request.user)

class UserFavoriteQuestionList(ListView):
    template_name = 'profiles/favorite_questions.html'
    model = Question
    context_object_name = 'question_list'
    paginate_by = 10

    def get_queryset(self):
        questions = Question.published.filter(votes__vote=1, votes__user=self.request.user)
        return questions

def profile_edit_view(request):

    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user, 
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile, 
            data=request.POST, 
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'profiles/profile_edit_form.html', context={'user_form': user_form, 
                                                                       'profile_form': profile_form})
