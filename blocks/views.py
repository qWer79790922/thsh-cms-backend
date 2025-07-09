from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ContentBlock
from .serializers import ContentBlockSerializer


class ContentBlockListView(generics.ListAPIView):
    queryset = ContentBlock.objects.filter(is_published=True).order_by('position')
    serializer_class = ContentBlockSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        section = self.request.query_params.get('section')
        if section:
            queryset = queryset.filter(section=section)
        return queryset