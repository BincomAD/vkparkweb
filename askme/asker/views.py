from django.shortcuts import render
def index(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i)
        })
    context = {'questions': questions}
    return render(request, 'index.html', context)

def hot(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
        })
    context = {'questions': questions}
    return render(request, 'hot.html', context)

def tag(request, tag_name):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'title ' + str(i),
            'id': i,
            'text': 'text' + str(i),
        })
    context = {'questions': questions, 'tag_name': tag_name}
    return render(request, 'tag.html', context)

def question(request, question_id):
    question = {
        'title': 'title ' + str(question_id),
        'id': question_id,
        'text': 'text' + str(question_id),
        'answers': []
    }
    for i in range(1, 6):
        question['answers'].append({
            'text': 'answer ' + str(i),
            'id': i,
        })
    context = {'question': question}
    return render(request, 'question.html', context)

def ask(request):
    return render(request,'ask.html')

def login(request):
    return render(request,'login.html')

def registration(request):
    return render(request,'registration.html')

def settings(request):
    return render(request,'settings.html')
