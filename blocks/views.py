from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import ContentBlock, BlockTitle, BlockText, BlockImage
from .serializers import  (
    ContentBlockSerializer,
    BlockTitleSerializer,
    BlockTextSerializer,
    BlockImageSerializer,
)



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
    
class ContentBlockCreateView(APIView):
    def post(self, request, *args, **kwargs):
        block_type = request.data.get('block_type')

        # 先建立 ContentBlock 主資料
        content_block_data = {
            key: request.data.get(key)
            for key in ['section', 'block_type', 'position', 'is_published']
        }
        content_block = ContentBlock.objects.create(**content_block_data)

        # 根據 block_type 建立對應的積木
        if block_type == 'title':
            title_data = request.data.get('title')
            if title_data:
                BlockTitle.objects.create(block=content_block, **title_data)

        elif block_type == 'text':
            text_data = request.data.get('text')
            if text_data:
                BlockText.objects.create(block=content_block, **text_data)

        elif block_type == 'image':
            image_data = request.data.get('image')
            if image_data:
                BlockImage.objects.create(block=content_block, **image_data)

        else:
            return Response(
                {"detail": f"Unsupported block_type: {block_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 回傳完整 block 資料
        serializer = ContentBlockSerializer(content_block)
        return Response(serializer.data, status=status.HTTP_201_CREATED)