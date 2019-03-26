from rest_framework.generics import CreateAPIView

from ..serializers.rating import RatingSerializer
from ..serializers.skip_rating import SkipRatingSerializer


class RatingCreateView(CreateAPIView):
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkipRatingCreateView(CreateAPIView):
    serializer_class = SkipRatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
