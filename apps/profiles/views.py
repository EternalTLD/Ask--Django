from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models.query import QuerySet
from django.db import transaction
from django.db.models import Count, Q, Prefetch

from apps.users.models import User
from apps.questions.models import Question
from .forms import UserEditForm, ProfileEditForm


class ProfileDetailView(generic.DetailView):
    template_name = "profiles/profile_detail.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"

    def get_object(self) -> User:
        username = self.kwargs.get("username")
        return get_object_or_404(
            self.model.objects.select_related("profile").prefetch_related(
                Prefetch(
                    "questions", queryset=Question.objects.prefetch_related("tags")
                )
            ),
            username=username,
        )


class UserFavoriteQuestionList(generic.ListView):
    template_name = "profiles/favorite_questions.html"
    model = Question
    context_object_name = "question_list"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Question]:
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        questions = (
            Question.published.get_all_questions()
            .annotate(
                vote_count=Count("votes", filter=Q(votes__vote=1, votes__user=user))
            )
            .filter(vote_count__gt=0)
        )
        return questions


@transaction.atomic
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "profiles/profile_edit_form.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )
