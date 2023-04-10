from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
def index(request):
    questions = []
    questions_list = Question.questions.new()
    for i in questions_list:
        question = i
        user = Profile.objects.get(user=question.user)
        answers = Answer.objects.filter(question=i)
        questions.append({
            'title': question.title,
            'id': question.id,
            'text': question.text,
            'tags': question.tags.all(),
            'avatar': user.avatar,
            'rating': question.rating,
            'answers': answers.count()
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects}
    return render(request, 'index.html', context)

def hot(request):
    questions = []
    questions_list = Question.questions.best()
    for i in questions_list:
        question = i
        user = Profile.objects.get(user=question.user)
        answers = Answer.objects.filter(question=i)
        questions.append({
            'title': question.title,
            'id': question.id,
            'text': question.text,
            'tags': question.tags.all(),
            'avatar': user.avatar,
            'rating': question.rating,
            'answers': answers.count()
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects}
    return render(request, 'hot.html', context)

def tag(request, tag_name):
    questions = []
    questions_list = Question.objects.filter(tags__name__exact = tag_name)
    for i in questions_list:
        question = i
        user = Profile.objects.get(user=question.user)
        answers = Answer.objects.filter(question=i)
        questions.append({
            'title': question.title,
            'id': question.id,
            'text': question.text,
            'tags': question.tags.all(),
            'avatar': user.avatar,
            'rating': question.rating,
            'answers': answers.count()
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects, 'tag_name': tag_name}
    return render(request, 'tag.html', context)

def question(request, question_id):
    questionCurr = Question.objects.get(id = question_id)
    userQuest = Profile.objects.get(user=questionCurr.user)
    question = {
        'title': questionCurr.title,
        'id': questionCurr.id,
        'text': questionCurr.text,
        'answers': [],
        'tags': questionCurr.tags.all(),
        'avatar': userQuest.avatar,
        'rating': questionCurr.rating,
    }
    for i in Answer.objects.filter(question=questionCurr):
        userAnsw = Profile.objects.get(user= i.user)
        question['answers'].append({
            'text': i.text,
            'id': i.id,
            'rating': i.rating,
            'avatar': userAnsw.avatar,

        })
        objects = paginate(question['answers'], request, 5)
    context = {'question': question, 'questions': objects}
    return render(request, 'question.html', context)

def ask(request):
    return render(request,'ask.html')

def login(request):
    return render(request,'login.html')

def registration(request):
    return render(request,'registration.html')

def settings(request):
    return render(request,'settings.html')

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return objects
