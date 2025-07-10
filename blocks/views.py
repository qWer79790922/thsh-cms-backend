from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from .models import ContentBlock
from .serializers import ContentBlockSerializer
from .utils import create_nested_block, update_nested_block, build_fake_block


class ContentBlockListView(generics.ListAPIView):
    queryset = ContentBlock.objects.filter(is_published=True).order_by('position')
    serializer_class = ContentBlockSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        section = self.request.query_params.get('section')
        if section:
            queryset = queryset.filter(section=section)
        preview = self.request.query_params.get('preview')
        if preview != 'true': 
            queryset = queryset.filter(is_published=True)
        return queryset
    
class ContentBlockCreateView(APIView):
    def post(self, request, *args, **kwargs):
        block_type = request.data.get('block_type')

        content_block_data = {
            key: request.data.get(key)
            for key in ['section', 'block_type', 'position', 'is_published']
        }
        block = ContentBlock.objects.create(**content_block_data)

        create_nested_block(block_type, block, request.data)

        serializer = ContentBlockSerializer(block)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class ContentBlockUpdateView(RetrieveUpdateAPIView):
    queryset = ContentBlock.objects.all()
    serializer_class = ContentBlockSerializer

    def patch(self, request, *args, **kwargs):
        block = self.get_object()

        for field in ['section', 'position', 'is_published']:
            if field in request.data:
                setattr(block, field, request.data[field])
        block.save()

        update_nested_block(block.block_type, block, request.data)

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

            block = ContentBlock.objects.create(
                section=section,
                block_type=block_type,
                position=position,
                is_published=is_published
            )

            create_nested_block(block_type, block, block_data)
            created_blocks.append(block)

        serializer = ContentBlockSerializer(created_blocks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from .utils import update_nested_block

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
                continue

            # 更新主資料
            for field in ['position', 'is_published']:
                if field in block_data:
                    setattr(block, field, block_data[field])
            block.save()

            update_nested_block(block.block_type, block, block_data)

            updated_blocks.append(block)

        serializer = ContentBlockSerializer(updated_blocks, many=True)
        return Response(serializer.data)

class ContentBlockPreviewView(APIView):
    def post(self, request):
        section = request.data.get('section')
        blocks_data = request.data.get('blocks', [])
        preview_result = []

        for block_data in blocks_data:
            block_type = block_data.get('block_type')
            position = block_data.get('position', 0)
            fake_block = build_fake_block(block_type, section, position, block_data)
            preview_result.append(fake_block)

        serializer = ContentBlockSerializer(preview_result, many=True)
        return Response(serializer.data)