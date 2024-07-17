from django.contrib import admin
from .models import QuestionsModel, AnswerModel, CategoryQuestionModel, ResultTableModel,GroupResultsModel

# Register your models here.
admin.site.register(QuestionsModel)
admin.site.register(AnswerModel)
admin.site.register(CategoryQuestionModel)
admin.site.register(ResultTableModel)
admin.site.register(GroupResultsModel)