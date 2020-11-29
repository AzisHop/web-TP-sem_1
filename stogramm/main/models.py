from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings


#
#
# # Model Managers
#
# class ProfileManager(models.Manager):
#     def user_top(self):
#         return self.order_by('-rating')[:8]


class Profile(User):
    avatar = models.CharField(max_length=64, verbose_name="Путь к изображению", blank=True)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # rating = models.IntegerField(default=0)

    # objects = ProfileManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class AnswerManager(models.Manager):
    def answers_by_questions(self, id):
        return self.filter(question__id=id)


class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="Prof", default=0)
    text = models.TextField(verbose_name='Content')
    likes = models.ManyToManyField("Profile", through="AnswerLike",
                                   through_fields=("answer", "profile"),
                                   related_name="answer_liked")
    rating = models.IntegerField(verbose_name="Rating", default=0)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='creation_date')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.all().order_by('-date')

    def hot_questions(self):
        return self.all().order_by('-rating')

    def by_tag(self, tag):
        return self.filter(tags__text__exact=tag)


class Tag(models.Model):
    text = models.CharField(max_length=40, unique=True, verbose_name="tag_name")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=255, null=False, verbose_name='title')
    text = models.TextField(verbose_name='content')
    profile_asked = models.ForeignKey("Profile", on_delete=models.CASCADE,
                                      related_name="question_asked",
                                      default=0)

    likes = models.ManyToManyField("Profile", through="QuestionLike",
                                   through_fields=("question", "profile"),
                                   related_name="question_liked")

    rating = models.IntegerField(default=0, verbose_name='rating')
    tags = models.ManyToManyField("Tag", related_name="questions")
    date = models.DateField(auto_now_add=True, verbose_name='creation_date')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class QuestionLike(models.Model):
    LIKE = "+"
    DISLIKE = "-"
    RATINGS = [(LIKE, "Like"), (DISLIKE, "Dislike")]

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, default=0)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATINGS, default=LIKE)

    def __str__(self):
        return self.question.text

    class Meta:
        verbose_name = "Rating question"
        verbose_name_plural = "Rating questions"
        unique_together = (("profile", "question"),)


class AnswerLike(models.Model):
    LIKE = "+"
    DISLIKE = "-"
    RATINGS = [(LIKE, "Like"), (DISLIKE, "Dislike")]

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, default=0)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATINGS, default=LIKE)

    def __str__(self):
        return self.answer.text

    class Meta:
        verbose_name = "Рейтинг ответа"
        verbose_name_plural = "Рейтинг ответов"
        unique_together = (("profile", "answer"),)
