from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question_detail = get_object_or_404(Question, pk=question_id)
    context = {'question': question_detail}
    return render(request, 'polls/detail.html', context)

def result(request, question_id, choice_id):
    question = Question.objects.get(pk=question_id)
    choice = Choice.objects.get(pk=choice_id)
    context = {'question': question, 'choice': choice}
    # response = "ID %s번 설문에 참여하셨습니다."
    # return HttpResponse(response % question_id)
    return render(request, 'polls/result.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "!답변을 선택해주세요!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,selected_choice.id)))