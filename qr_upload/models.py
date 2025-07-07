# qr_upload/models.py
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class QrTemporaryLink(models.Model): # 기존 TemporaryLink와 이름 충돌 방지
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    filename = models.CharField(max_length=255) # 어떤 파일명으로 S3에 업로드될지
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    # 한 번 사용되면 비활성화
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk: # 새로 생성될 때만 expires_at 설정
            # 예: 링크 유효 기간을 1시간 (60분)으로 설정
            self.expires_at = timezone.now() + timedelta(minutes=60)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"QR Link for {self.filename} (Active: {self.is_active}, Used: {self.is_used}, Expires: {self.expires_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "QR 임시 링크"
        verbose_name_plural = "QR 임시 링크"

