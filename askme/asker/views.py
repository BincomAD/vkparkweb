from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def index(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
            'tags': ["black_jack", "black_jack"]
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects}
    return render(request, 'index.html', context)

def hot(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
            'tags': ["black_jack", "black_jack"]
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects}
    return render(request, 'hot.html', context)

def tag(request, tag_name):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
            'tags': ["black_jack", "black_jack"]
        })
    objects = paginate(questions, request, 5)
    context = {'questions': objects, 'tag_name': tag_name}
    return render(request, 'tag.html', context)

def question(request, question_id):
    question = {
        'title': 'title ' + str(question_id),
        'id': question_id,
        'text': 'text' + str(question_id),
        'answers': [],
        'tags': ["black_jack","black_jack"]
    }
    for i in range(1, 21):
        question['answers'].append({
            'text': 'answer ' + str(i),
            'id': i,
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
