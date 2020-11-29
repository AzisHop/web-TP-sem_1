from django.contrib import admin

# Register your models here.
from main import models

admin.site.register(models.Profile)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.AnswerLike)
admin.site.register(models.QuestionLike)
admin.site.register(models.Tag)