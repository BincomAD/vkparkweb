from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from asker.models import Question, Answer, Tag, Like, Profile
from random import randint
import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', default=1, type=int)

    def handle(self, *args, **options):
        ratio = options.get('ratio', 1)
        num_users = 10 * ratio
        num_questions = 10 * ratio
        num_answers = 100 * ratio
        num_tags = 1 * ratio
        num_likes = 20 * ratio

        # create users
        for i in range(num_users):
            username = f'user{i}'
            password = 'password'
            email = f'user{i}@example.com'
            User.objects.create_user(username, email, password)
            avatar = f'/static/Uploads/avatar/{randint(1,4)}.png'
            nickname = f'nickname{i}'
            Profile.objects.create(user = User.objects.get(username=username),avatar = avatar, nickname = nickname)

        # create tags
        for i in range(num_tags):
            name = f'tag{i}'
            Tag.objects.create(name=name)

        # create questions
        for i in range(num_questions):
            textTitle = f'Title {i}'
            title = f'{textTitle}'
            textQuestion = f'question {i}'
            author_id = randint(0, num_users-1)
            text = f'{textQuestion}'
            user = User.objects.get(username=f'user{author_id}')
            question = Question.objects.create(id = i, user=user, text=text, title=title)

            # add tags to question
            for j in range(randint(1, 5)):
                tag_id = randint(0, num_tags-1)
                tag = Tag.objects.get(name=f'tag{tag_id}')
                question.tags.add(tag)

            question.save()


        # create answers
        for i in range(num_answers):
            textAnswer = f'Answer {i}'
            author_id = randint(0, num_users-1)
            question_id = randint(0, num_questions-1)
            question = Question.objects.get(id = question_id)
            text = f'{textAnswer}'
            user = User.objects.get(username=f'user{author_id}')
            Answer.objects.create(id = i, user=user, question=question, text=text)

        # create likes
        for i in range(num_likes):
            answer_id = randint(0, num_answers-1)
            question_id = randint(0, num_questions-1)
            user = User.objects.get(username=f'user{author_id}')
            Like.objects.create(user=user, answer=Answer.objects.get(pk=answer_id), question=Question.objects.get(pk=question_id))

        for i in range(num_questions):
            rating = Like.objects.filter(question = Question.objects.get(id = i)).count()
            question = Question.objects.get(id=i)
            question.rating = rating
            question.save()

        for i in range(num_answers):
            rating = Like.objects.filter(answer = Answer.objects.get(id = i)).count()
            answer = Answer.objects.get(id=i)
            answer.rating = rating
            answer.save()

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with test data.'))