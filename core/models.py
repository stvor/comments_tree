from django.db import models


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'

    text = models.TextField(verbose_name='Текст')
    parent = models.ForeignKey('self', verbose_name='Родительский коммент', blank=True, null=True,
                               help_text='Пустое значение означает, что родительского нет', on_delete=models.CASCADE)

    created = models.DateTimeField(verbose_name='Создано в', auto_now_add=True, db_index=True)
    updated = models.DateTimeField(verbose_name='Изменено в', auto_now=True)
    is_deleted = models.BooleanField(verbose_name='Удалено?', default=False)

    def __str__(self):
        return f'Коммент id={self.id}'
