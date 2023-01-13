from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choices


class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """Return the last live published questions."""
    return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/results.html"


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choices_set.get(pk=request.POST['choice_form'])
  except (KeyError, Choices.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': 'No elegiste una respuesta'
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=[question.id]))
