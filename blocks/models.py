from django.db import models


class ContentBlock(models.Model):
    section = models.CharField(max_length=255, blank=True, null=True)
    block_type = models.CharField(max_length=255)  # e.g., "title", "text", "image"
    position = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.section} - {self.block_type} ({self.id})"


class BlockTitle(models.Model):
    block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, related_name='titles')
    title_zh = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, default='h2')  # e.g., h1, h2, h3
    align = models.CharField(max_length=255, default='left')  # e.g., left, center, right

    def __str__(self):
        return self.title_zh


class BlockText(models.Model):
    block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, related_name='texts')
    text_zh = models.TextField()
    text_en = models.TextField(blank=True, null=True)
    is_rich = models.BooleanField(default=False)

    def __str__(self):
        return self.text_zh[:20]


class BlockImage(models.Model):
    block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()  # 儲存 Cloudinary 圖片 URL
    caption_zh = models.CharField(max_length=255, blank=True, null=True)
    caption_en = models.CharField(max_length=255, blank=True, null=True)
    align = models.CharField(max_length=255, default='center')

    def __str__(self):
        return self.image