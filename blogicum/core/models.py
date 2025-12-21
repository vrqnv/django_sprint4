from django.db import models


class IsPublishedMixin(models.Model):
    """Абстрактная модель. Добавляет флаг is_published."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    """Абстрактная модель. Добавляет поле created_at."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True

