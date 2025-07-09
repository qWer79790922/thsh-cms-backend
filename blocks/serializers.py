from rest_framework import serializers
from .models import (
    ContentBlock,
    BlockTitle,
    BlockText,
    BlockImage,
)


# ========== 子積木序列化器 ==========
class BlockTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockTitle
        exclude = ['id', 'block']


class BlockTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockText
        exclude = ['id', 'block']


class BlockImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockImage
        exclude = ['id', 'block']


# ========== 主 ContentBlock 序列化器 ==========

class ContentBlockSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ContentBlock
        fields = [
            'id', 'section', 'block_type', 'position', 'is_published',
            'title', 'text', 'image'
        ]

    def get_title(self, obj):
        if obj.block_type == 'title':
            title = BlockTitle.objects.filter(block=obj).first()
            return BlockTitleSerializer(title).data if title else None
        return None

    def get_text(self, obj):
        if obj.block_type == 'text':
            text = BlockText.objects.filter(block=obj).first()
            return BlockTextSerializer(text).data if text else None
        return None

    def get_image(self, obj):
        if obj.block_type == 'image':
            image = BlockImage.objects.filter(block=obj).first()
            return BlockImageSerializer(image).data if image else None
        return None