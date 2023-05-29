from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.SlugField(
        verbose_name='Логин',
        max_length=settings.EMAIL_MAX_LEN,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.USER_FIELDS_MAX_LEN,
        unique=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.USER_FIELDS_MAX_LEN,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.USER_FIELDS_MAX_LEN,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.USER_FIELDS_MAX_LEN,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписок пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_follow'),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return (
            f'{self.user.username}'
            f' подписан на {self.author.username}'
        )
