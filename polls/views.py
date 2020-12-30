from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from polls.models import Choice, Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
# def index(request):
#     latest_questions = Question.objects.order_by("-pub_date")[:5]
#     return render(request, "polls/index.html", {"latest_questions": latest_questions})


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        """
        returns the last 5 published questions not including future ones
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Exclude any future questions
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request, "polls/detail.html", {"error_message": "Please pick a choice!"}
        )
    else:
        selected.votes += 1
        selected.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
