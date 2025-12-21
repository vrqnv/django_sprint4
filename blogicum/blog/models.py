from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from core.models import IsPublishedMixin, CreatedAtMixin

User = get_user_model()


class PublishedManager(models.Manager):
    """Менеджер для фильтрации опубликованных постов."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
        )


class Category(IsPublishedMixin, CreatedAtMixin):
    """Тематическая категория"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(IsPublishedMixin, CreatedAtMixin):
    """Географическая метка"""

    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(IsPublishedMixin, CreatedAtMixin):
    """Публикация"""

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(
        upload_to="posts_images/", blank=True, verbose_name="Изображение"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.id})


class Comment(CreatedAtMixin):
    """Комментарий к публикации"""

    text = models.TextField("Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор комментария"
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий {self.author} к {self.post}"
