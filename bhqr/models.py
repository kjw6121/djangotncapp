# models.py

from django.db import models, connection
from django.contrib.auth.models import User



class ScanData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_message = models.CharField(max_length=255)
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scan_message} - {self.scan_time}"
    
class today_scandata(models.Model):
    username = models.CharField(max_length=255)
    scan_message = models.CharField(max_length=255)
    scan_time = models.DateTimeField(auto_now_add=True)
   
    @staticmethod
    def call_stored_procedure():
        with connection.cursor() as cursor:
            cursor.execute("EXEC bhqrscan")
            results = cursor.fetchall()
            
        return results