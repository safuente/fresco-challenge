from rest_framework import (
    viewsets
)
# Create your views here.
from recipes import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        queryset = self.queryset

        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
