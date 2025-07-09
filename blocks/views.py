from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from .models import ContentBlock, BlockTitle, BlockText, BlockImage
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
    
class ContentBlockUpdateView(RetrieveUpdateAPIView):
    queryset = ContentBlock.objects.all()
    serializer_class = ContentBlockSerializer

    def patch(self, request, *args, **kwargs):
        block = self.get_object()

        # 更新 ContentBlock 本體
        for field in ['section', 'position', 'is_published']:
            if field in request.data:
                setattr(block, field, request.data[field])
        block.save()

        # 根據 block_type 更新對應積木
        if block.block_type == 'title':
            title = BlockTitle.objects.filter(block=block).first()
            if title and 'title' in request.data:
                for k, v in request.data['title'].items():
                    setattr(title, k, v)
                title.save()

        elif block.block_type == 'text':
            text = BlockText.objects.filter(block=block).first()
            if text and 'text' in request.data:
                for k, v in request.data['text'].items():
                    setattr(text, k, v)
                text.save()

        elif block.block_type == 'image':
            image = BlockImage.objects.filter(block=block).first()
            if image and 'image' in request.data:
                for k, v in request.data['image'].items():
                    setattr(image, k, v)
                image.save()

        serializer = self.get_serializer(block)
        return Response(serializer.data)
    
class ContentBlockBatchCreateView(APIView):
    def post(self, request):
        section = request.data.get('section')
        blocks_data = request.data.get('blocks', [])
        created_blocks = []

        for block_data in blocks_data:
            block_type = block_data.get('block_type')
            position = block_data.get('position')
            is_published = block_data.get('is_published', True)

            content_block = ContentBlock.objects.create(
                section=section,
                block_type=block_type,
                position=position,
                is_published=is_published
            )

            if block_type == 'title':
                BlockTitle.objects.create(block=content_block, **block_data['title'])

            elif block_type == 'text':
                BlockText.objects.create(block=content_block, **block_data['text'])

            elif block_type == 'image':
                BlockImage.objects.create(block=content_block, **block_data['image'])

            created_blocks.append(content_block)

        serialized = ContentBlockSerializer(created_blocks, many=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class ContentBlockBatchUpdateView(APIView):
    def patch(self, request):
        section = request.data.get('section')
        blocks_data = request.data.get('blocks', [])
        updated_blocks = []

        for block_data in blocks_data:
            block_id = block_data.get('id')
            try:
                block = ContentBlock.objects.get(id=block_id, section=section)
            except ContentBlock.DoesNotExist:
                continue  # 忽略不存在的資料

            # 更新主資料
            for field in ['position', 'is_published']:
                if field in block_data:
                    setattr(block, field, block_data[field])
            block.save()

            # 更新子積木內容
            if block.block_type == 'title':
                title = BlockTitle.objects.filter(block=block).first()
                if title and 'title' in block_data:
                    for k, v in block_data['title'].items():
                        setattr(title, k, v)
                    title.save()

            elif block.block_type == 'text':
                text = BlockText.objects.filter(block=block).first()
                if text and 'text' in block_data:
                    for k, v in block_data['text'].items():
                        setattr(text, k, v)
                    text.save()

            elif block.block_type == 'image':
                image = BlockImage.objects.filter(block=block).first()
                if image and 'image' in block_data:
                    for k, v in block_data['image'].items():
                        setattr(image, k, v)
                    image.save()

            updated_blocks.append(block)

        serializer = ContentBlockSerializer(updated_blocks, many=True)
        return Response(serializer.data)