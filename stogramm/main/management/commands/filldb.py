from sys import exit
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils import timezone
import django.apps
import datetime
from main import models
from faker import Faker
from random import choice, sample, randint
from faker.providers import *
import math


# TODO: Tags and ManyToMany Linkage!
class Command(BaseCommand):
    help = "This will not help you"

    def add_arguments(self, parser):
        parser.add_argument("size", nargs='+', type=str)

    def handle(self, *args, **options):
        if options["size"][0] == "small":
            usersAmount = 100
            questionsAmount = 20
            answersAmount = 100
            tagsAmount = 30
            usersLikesAmount = 50
        elif options["size"][0] == "medium":
            usersAmount = 1001
            questionsAmount = 10001
            answersAmount = 100001
            tagsAmount = 10000
            usersLikesAmount = 100001
        elif options["size"][0] == "big":
            usersAmount = 10001
            questionsAmount = 100001
            answersAmount = 1000001
            tagsAmount = 10001
            usersLikesAmount = 2000001
        else:
            self.stdout.write("Usage: filldb small(medium, big)")
            exit()

        fake = Faker()

        tags = {(fake.job().split()[0].replace("/", " ")) for i in range(tagsAmount)}
        models.Tag.objects.bulk_create((models.Tag(text=tag)) for tag in (tags))
        tagsIDs = models.Tag.objects.values_list("id", flat=True)

        profiles = [models.Profile(username=fake.unique.name(),
                                   password=fake.password(),
                                   date_joined=fake.date_this_year())
                    for i in range(usersAmount)]
        # Because of "ValueError: Can't bulk create a multi-table inherited model"
        for profile in profiles:
            profile.save()
        profileIDs = models.Profile.objects.values_list("id", flat=True)

        questions = [models.Question(title=fake.sentence()[:32],
                                     text=fake.text()[:128],
                                     profile_asked_id=choice(profileIDs),
                                     date=fake.date_this_year())
                     for i in range(questionsAmount)]
        models.Question.objects.bulk_create(questions)
        questionIDs = models.Question.objects.values_list("id", flat=True)

        for question in models.Question.objects.all():
            averageTags = math.ceil(tagsAmount / questionsAmount)
            for i in sample(list(tagsIDs), randint(averageTags - 2, averageTags + 2)):
                question.tags.add(i)

        answers = [models.Answer(question_id=choice(questionIDs),
                                 profile_id=choice(profileIDs),
                                 text=fake.text()[:128])
                   for i in range(answersAmount)]
        models.Answer.objects.bulk_create(answers)

        answerlikes = []
        answers = []
        for answer in models.Answer.objects.all():
            pids = sample(list(profileIDs), randint(int(0.25 * usersAmount), int(0.75 * usersAmount)))
            summRating = 0
            for pid in pids:
                rating = choice(["+", "-"])
                if rating == "+":
                    summRating += 1
                else:
                    summRating -= 1
                answerlikes.append(models.AnswerLike(
                    rating=rating,
                    answer_id=answer.id,
                    profile_id=pid))
                answer.rating = summRating
                answers.append(answer)
        models.AnswerLike.objects.bulk_create(answerlikes)
        models.Answer.objects.bulk_update(answers, ["rating"])

        questionlikes = []
        questions = []
        for question in models.Question.objects.all():
            pids = sample(list(profileIDs), randint(int(0.25 * usersAmount), int(0.75 * usersAmount)))
            summRating = 0
            for pid in pids:
                rating = choice(["+", "-"])
                if rating == "+":
                    summRating += 1
                else:
                    summRating -= 1
                questionlikes.append(models.QuestionLike(
                    rating=rating,
                    question_id=question.id,
                    profile_id=pid))
                question.rating = summRating
                questions.append(question)
        models.QuestionLike.objects.bulk_create(questionlikes)
        models.Question.objects.bulk_update(questions, ["rating"])

        self.stdout.write(self.style.SUCCESS(f"{options['size'][0]} preset was created"))