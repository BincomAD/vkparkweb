from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as auth_login
from .forms import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
            'avatar': user.avatar.url,
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
    questionCurr = Question.objects.get(id=question_id)
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
        userAnsw = Profile.objects.get(user=i.user)
        question['answers'].append({
            'text': i.text,
            'id': i.id,
            'rating': i.rating,
            'avatar': userAnsw.avatar,
        })

    paginator = Paginator(question['answers'], 5)
    page_number = request.GET.get('page')
    objects = paginator.get_page(page_number)

    context = {'question': question, 'questions': objects, 'profile': userQuest}
    return render(request, 'question.html', context)



def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user

            # Сохраняем введенные теги и связываем их с вопросом
            tags = form.cleaned_data.get('tags')  # Получаем выбранные теги из формы
            question.save()  # Сохраняем вопрос

            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)  # Получаем или создаем тег по имени
                question.tags.add(tag)  # Связываем вопрос с тегом

            return redirect('question', question_id=question.pk)  # Перенаправляем на страницу вопроса
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Используем явное указание модуля
                return redirect(request.GET.get('continue', '/'))
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Создание профиля и связывание с пользователем
            profile = Profile(user=user, avatar=request.FILES.get('avatar'), nickname=form.cleaned_data['nickname'])
            profile.save()

            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'registration.html', {'form': form})
def settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'settings.html', {'form': form})


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

def add_answer(request, question_id):
    if request.method == 'POST':
        answer_text = request.POST.get('answer')
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(text=answer_text, user=request.user, question=question)
        return redirect(reverse('question', args=[question_id]) + f'#{answer.id}')

@csrf_exempt
def like_question(request):
    if request.method == 'POST' and request.is_ajax():
        question_id = request.POST.get('id')
        like_type = request.POST.get('type')

        question = get_object_or_404(Question, id=question_id)

        # Проверяем, лайкал ли пользователь уже данный вопрос
        like, created = Like.objects.get_or_create(user=request.user, question=question)
        if like_type == 'like':
            if not created and like.like_type == 'like':
                return JsonResponse({'error': 'You have already liked this question.'})
            like.like_type = 'like'
            question.rating += 1
        elif like_type == 'dislike':
            if not created and like.like_type == 'dislike':
                return JsonResponse({'error': 'You have already disliked this question.'})
            like.like_type = 'dislike'
            question.rating -= 1

        question.save()
        like.save()

        return JsonResponse({'rating': question.rating})

    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def select_correct_answer(request):
    if request.method == 'POST' and request.is_ajax():
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')

        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        # Проверяем, является ли пользователь автором вопроса
        if request.user != question.user:
            return JsonResponse({'error': 'Only the author of the question can select the correct answer.'})

        question.correct_answer = answer
        question.save()

        return JsonResponse({'success': 'Correct answer has been selected.'})

    return JsonResponse({'error': 'Invalid request'})