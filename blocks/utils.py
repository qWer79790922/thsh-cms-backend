from .models import BlockTitle, BlockText, BlockImage, ContentBlock


def create_nested_block(block_type, block, data):
    """
    建立對應的巢狀積木資料（title / text / image）
    """
    if block_type == 'title':
        BlockTitle.objects.create(block=block, **data.get('title', {}))
    elif block_type == 'text':
        BlockText.objects.create(block=block, **data.get('text', {}))
    elif block_type == 'image':
        BlockImage.objects.create(block=block, **data.get('image', {}))
    else:
        raise ValueError(f"Unsupported block_type: {block_type}")


def update_nested_block(block_type, block, data):
    """
    更新對應的巢狀積木資料（title / text / image）
    """
    if block_type == 'title':
        instance = BlockTitle.objects.filter(block=block).first()
        content = data.get('title')
    elif block_type == 'text':
        instance = BlockText.objects.filter(block=block).first()
        content = data.get('text')
    elif block_type == 'image':
        instance = BlockImage.objects.filter(block=block).first()
        content = data.get('image')
    else:
        raise ValueError(f"Unsupported block_type: {block_type}")

    if instance and content:
        for k, v in content.items():
            setattr(instance, k, v)
        instance.save()


def build_fake_block(block_type, section, position, content, is_published=False):
    """
    建立模擬用 ContentBlock（不儲存 DB）供即時預覽使用
    """
    block = ContentBlock(
        id=None,
        section=section,
        block_type=block_type,
        position=position,
        is_published=is_published
    )

    if block_type == 'title':
        block.title = BlockTitle(**content.get('title', {}))
    elif block_type == 'text':
        block.text = BlockText(**content.get('text', {}))
    elif block_type == 'image':
        block.image = BlockImage(**content.get('image', {}))
    else:
        raise ValueError(f"Unsupported block_type: {block_type}")

    return block