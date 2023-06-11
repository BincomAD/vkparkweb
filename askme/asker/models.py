from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

class QuestionManager(models.Manager):
    def best(self):
        return self.order_by('-rating', '-created_at')

    def new(self):
        return self.order_by('-created_at')

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    questions = QuestionManager()
    correct_answer = models.ForeignKey(
        'Answer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='correct_for_question'
    )

class Answer(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE  )
    avatar = models.ImageField(upload_to='Uploads/avatar/', default='Uploads/avatar/1.png')
    nickname = models.CharField(max_length=255, null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.avatar:
            self.avatar = 'Uploads/avatar/1.png'
            self.save()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
