from django.db import models

class ob(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(max_length=100)
    date = models.DateTimeField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'outbound_ob'
