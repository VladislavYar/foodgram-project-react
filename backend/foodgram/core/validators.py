from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError

from users.models import User


def validate_favorite_shopping_cart(data, request, model, message):
    """Валидирует actions-ы favorite и shopping_cart."""
    exists = model.objects.filter(
            user=request.user, recipe=data['recipe']
        ).exists()
    if exists and request.method == 'POST':
        raise ValidationError({'error': f'Блюдо уже в списке {message}'})
    elif not exists and request.method == 'DELETE':
        raise ValidationError({'error': f'Блюда нет в списке {message}'})
    return data


def validate_subscribe(context):
    """Валидирует actions-ы favorite и shopping_cart."""
    author_id = context.get('view').kwargs.get('id')
    author = get_object_or_404(User, pk=author_id)
    user = context.get('request').user
    is_follower = user.follower.filter(author=author_id)
    method = context.get('request').method

    if user == author and method == 'POST':
        raise ValidationError(
            {'error': 'Подписка на самого себя запрещена'}
            )
    elif is_follower and method == 'POST':
        raise ValidationError({'error': 'Вы уже подписаны на автора'})
    elif not is_follower and method == 'DELETE':
        raise ValidationError({'error': 'Вы не подписаны на автора'})
    return {'author': author, 'user': user}
