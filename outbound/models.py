from django.db import models
from django.db import models, connection

class ob(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=100)
    date = models.DateTimeField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'outbound_ob'

  
class ob_today_scandata(models.Model):
    user = models.CharField(max_length=100)
    date = models.DateTimeField()
    name = models.TextField()
   
    @staticmethod
    def call_stored_procedure():
        with connection.cursor() as cursor:
            cursor.execute("obscan")
            results = cursor.fetchall()
            
        return results
