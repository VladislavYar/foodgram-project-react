from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def action_shopping_cart_fovorite(request, pk, serializer, model):
    """Action добавления/удаления подписок, покупок."""
    data = {'recipe': pk, 'user': request.user.pk}
    serializer = serializer(data=data, context={'request':
                            request})
    serializer.is_valid(raise_exception=True)
    if request.method == 'POST':
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        get_object_or_404(model, recipe=pk,
                          user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
