from rest_framework import status
from rest_framework.response import Response


def action_post_delete(obj, serializer, instance):
    """Создание, удаление для списка покупок, избранного, подписок."""
    request = obj.request
    user = request.user
    recipe = obj.get_object()

    if request.method == 'POST':
        serializer = serializer(
            data={
                'user': user.id,
                'recipe': recipe.id
            },
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    if instance:
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
