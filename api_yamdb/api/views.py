from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# написать пермишн админ/модератор

from reviews.models import Review, Comment

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer # допишу позже
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)