# from django.http import HttpResponse

from django.core.paginator import Paginator
from django.shortcuts import render
from main import models


# class Answer(object):
#     def __init__(self, id, text, rating):
#         self.id = id
#         self.text = text
#         self.rating = rating
#
#
# class Question(object):
#     def __init__(self, id, title, text, tags, rating, answers):
#         self.id = id
#         self.title = title
#         self.text = text
#         self.tags = tags
#         self.rating = rating
#         self.answers = answers
#
#
# text1 = \
#     "In the U.S. getting a card isn’t as hard as it used to be. " \
#     "Some companies now mail applications to high school students," \
#     "At their worst, cards allow people with poor money management skills to get into a high-interest debt."
#
# text2 = \
#     "n other words, any American knows that how he or she handles their credit card or cards, " \
#     "either will help them or haunt them for years."
#
# text3 = \
#     "What makes every American a typical one is a desire to get a well-paid job that will cover their credit card." \
#     "A credit card is an indispensable part of life in America."
#
# answer0 = Answer(232, text1, 3)
# answer1 = Answer(213, text2, 2)
# answer2 = Answer(133, text3, 5)
#
# questions = [ Question(idx,
#                        f"Sorry, i don`t know what ask{idx}",
#                        f"What makes every American a typical one is a desire to get a well-paid "
#                        f"job that will cover their credit card",
#                        ["tesla", "space"],
#                        idx % 10,
#                        [answer0, answer0,answer1,answer0, answer0,answer1, answer2])
#               for idx in range(50)
#             ]


def index(request):
    objects_of_page = paginate(models.Question.objects.new_questions(), request)

    return render(request, 'main/index.html', {
        'objects_of_page': objects_of_page
    })


def hot(request):
    objects_of_page = paginate(models.Question.objects.hot_questions(), request)

    return render(request, 'main/hot.html', {
        'objects_of_page': objects_of_page
    })


# def registration(request):
#     return render(request, 'registration.html', {})


def ask(request):
    return render(request, 'main/ask.html', {})


def login(request):
    return render(request, 'main/login.html', {})


def settings(request):
    return render(request, 'main/settings.html', {})


def tag(request, tag):
    objects_of_page = paginate(models.Question.objects.by_tag(tag), request)

    return render(request, 'main/tag.html', {
        "tag": tag,
        "objects_of_page": objects_of_page,
    })


def question(request, question_id):
    objects_of_page = paginate(models.Answer.objects.answers_by_questions(question_id), request)

    return render(request, 'main/question.html', {
        'question': models.Question.objects.get(id=question_id),
        'objects_of_page': objects_of_page,
    })


def singup(request):
    return render(request, 'main/singup.html', {})


def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page')
    objects_of_page = paginator.get_page(page_number)
    return objects_of_page
