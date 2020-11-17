from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Model Managers

class Profile(User):
    avatar = models.FilePathField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.all().order_by('-creation_datetime')

    def hot_questions(self):
        return self.all().order_by('-rating')


# TODO sort_by_tag


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Question(models.Model):
    title = models.CharField(max_length=255, null=False, verbose_name='title')
    content = models.TextField(verbose_name='content')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='creation_date')
    rating = models.IntegerField(default=0, verbose_name='rating')

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Answer(models.Model):
    content = models.TextField(verbose_name='content')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='creation_date')
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'


class Question_Like(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = (("question", "user"),)


class Answer_Like(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = (("answer", "user"),)
