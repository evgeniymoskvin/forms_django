from django.db import models


# Create your models here.

class CategoryQuestionModel(models.Model):
    name_category = models.CharField(verbose_name="Наименование опроса", max_length=500)
    show = models.BooleanField(verbose_name="Проводится сейчас", default=True)

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = "опросы"

    def __str__(self):
        return f'{self.name_category}'


class QuestionsModel(models.Model):
    category_of_question = models.ForeignKey(CategoryQuestionModel, verbose_name='Опрос', default=None, null=True,
                                             blank=True, on_delete=models.CASCADE)
    question = models.CharField(verbose_name='Вопрос', max_length=500)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = "вопросы"

    def __str__(self):
        return f'{self.category_of_question} - {self.question}'


class AnswerModel(models.Model):
    question = models.ForeignKey(QuestionsModel, verbose_name='Вопрос', on_delete=models.CASCADE, default=None,
                                 null=True, blank=True)
    answer_code = models.IntegerField(verbose_name='Код варианта ответа')
    answer_text = models.CharField(verbose_name='Текст варианта ответа', max_length=200)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = "ответы"

    def __str__(self):
        return f'{self.question} - {self.answer_code} - {self.answer_text}'


class GroupResultsModel(models.Model):
    count_number = models.IntegerField(verbose_name='Порядковый номер')
    category_question = models.ForeignKey(CategoryQuestionModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'группа ответа'
        verbose_name_plural = "группы ответов"

    def __str__(self):
        return f'{self.count_number}'


class ResultTableModel(models.Model):
    group_number = models.ForeignKey(GroupResultsModel, verbose_name='Группа ответа', on_delete=models.SET_NULL,
                                     null=True, blank=True)
    question = models.ForeignKey(QuestionsModel, verbose_name='Вопрос', on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerModel, verbose_name='Ответ', on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.CharField(verbose_name='Текстовое поле ответа', max_length=150, default=None, null=True,
                                   blank=True)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = "результаты"

    def __str__(self):
        return f'{self.question} - {self.answer}'
