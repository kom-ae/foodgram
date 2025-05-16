from rest_framework import status
from rest_framework.response import Response


def action_post_delete(request, serializer, data, instance):
    """Создание, удаление для списка покупок, избранного, подписок."""

    if request.method == 'POST':
        serializer = serializer(
            data=data,
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
