# models.py

from django.db import models
from django.contrib.auth.models import User

class ScanData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_message = models.CharField(max_length=255)
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scan_message} - {self.scan_time}"
