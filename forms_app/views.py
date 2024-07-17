import ast

from django.shortcuts import render
from django.views import View
from .models import CategoryQuestionModel, QuestionsModel, AnswerModel, ResultTableModel, GroupResultsModel
from django.http import HttpResponse


# Create your views here.

class IndexView(View):
    """
    Главная страница проекта
    """

    def get(self, request):
        check_category = CategoryQuestionModel.objects.get_queryset().filter(show=True)[0]
        now_category = check_category.id
        try:
            done_test = int(request.COOKIES['done_test'])
        except:
            done_test = ''
        print(done_test)
        print(now_category)
        if done_test != now_category:

            questions = QuestionsModel.objects.get_queryset().filter(category_of_question_id=now_category)
            dict_of_questions = {}
            for question in questions:
                answers = AnswerModel.objects.get_queryset().filter(question=question)
                if len(answers) > 0:
                    dict_of_questions[question] = answers
                else:
                    dict_of_questions[question] = None

            name_of_category = check_category.name_category
            print(dict_of_questions)
            content = {
                'now_category': now_category,
                'name_of_category': name_of_category,
                'dict_of_questions': dict_of_questions
            }
            resp = render(request, 'forms_app/index.html', content)
            return resp
        else:
            content = {
                'now_category': now_category}
            resp = render(request, 'forms_app/test_done.html', content)
            return resp

    def post(self, request):
        print(request.POST)
        result_dict = dict(request.POST.lists())
        num_category = int(request.POST['obj_id'])
        del result_dict['csrfmiddlewaretoken']
        del result_dict['obj_id']
        print(result_dict)

        try:
            count_number = GroupResultsModel.objects.last().count_number
        except:
            count_number = 0
        count_number += 1
        new_count = GroupResultsModel(category_question_id=num_category,
                                      count_number=count_number)
        new_count.save()

        for key, value in result_dict.items():
            new_result = ResultTableModel()
            print(key, value)
            new_result.question_id = int(key)
            new_result.group_number_id = new_count.id
            try:
                answer_obj = AnswerModel.objects.get(id=int(value[0]))
                new_result.answer_id = int(value[0])
                print('added int')
            except:
                new_result.answer_text = str(value[0])
                print('added str')
            new_result.save()
        resp = HttpResponse(status=200)
        resp.set_cookie('done_test', num_category)
        return resp


class ShowCategoriesView(View):
    def get(self, request):
        categories = CategoryQuestionModel.objects.get_queryset()
        content = {'categories': categories}
        if request.user.is_authenticated:
            resp = render(request, 'forms_app/categories.html', content)
        else:
            resp = render(request, 'forms_app/error_permission.html', content)
        return resp


class ShowResultView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            columns = QuestionsModel.objects.get_queryset().filter(category_of_question=pk).order_by('id')
            answer_groups = GroupResultsModel.objects.get_queryset().filter(category_question=pk)
            answer_dict = {}
            for answ in answer_groups:
                temp_list = []
                results_answers = ResultTableModel.objects.get_queryset().filter(group_number_id=answ.id).order_by(
                    'question_id')
                answer_dict[answ.count_number] = results_answers

            content = {'name_of_category': CategoryQuestionModel.objects.get(id=pk).name_category,
                       'columns': columns,
                       'answer_dict': answer_dict,
                       'len_answer_dict': len(answer_dict)}
            resp = render(request, 'forms_app/results.html', content)
        else:
            content = {}
            resp = render(request, 'forms_app/error_permission.html', content)
        return resp
