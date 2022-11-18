# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()

    
def summary(self):
        return self.body[:30]




WET_YES = 'Yes'
WET_NO = 'No'

WET_CHOICES = [(WET_YES,'Yes'), (WET_NO, 'No')]

BOX_1='DN8 TILT'
BOX_2='YF TILT'
BOX_3='Height'
BOX_4='LX2_10'
BOX_5='LX2_12'
BOX_6='JOEM'
BOX_7='파워내장'
BOX_8='파워일반'
BOX_9='파워포장'
BOX_10='PU'
BOX_11='XMA'
BOX_12='일반히터'
BOX_13='GPB'
BOX_14='GPG'
BOX_15='기타'


 
BOX_CHOICES= [
    (BOX_1,'DN8 TILT'), (BOX_2,'YF TILT'), (BOX_3,'Height'),
     (BOX_4,'LX2_10'), (BOX_5,'LX2_12'), (BOX_6,'JOEM'), (BOX_7,'파워내장'), (BOX_8,'파워일반'), (BOX_9,'파워포장'), (BOX_10,'PU'), (BOX_11,'XMA'),
    (BOX_12,'일반히터'), (BOX_13,'GPB'), (BOX_14,'GPG'), (BOX_15, "기타")
       
    ]
 

INTEGER_CHOICES= [tuple([x,x]) for x in range(1,26)]


TIME_1='07:30' 
TIME_2='08:00' 
TIME_3='08:30' 
TIME_4='09:00' 
TIME_5='09:30'
TIME_6='10:00' 
TIME_7='10:30' 
TIME_8='11:00' 
TIME_9='11:30' 
TIME_10='12:00' 
TIME_11='12:30'
TIME_12='13:00' 
TIME_13='13:30'
TIME_14='14:00'
TIME_15='14:30'
TIME_16='15:00'
TIME_17='15:30'
TIME_18='16:00'
TIME_19='16:30'
TIME_20='17:00'
TIME_21='17:30'
TIME_22='18:00'
TIME_23='18:30'
TIME_24='19:00'

ARRIVAL_CHOICES= [(TIME_1, '07:30'),
                  (TIME_2, '08:00'), (TIME_3, '08:30'), (TIME_4, '09:00'), (TIME_5, '09:30'), (TIME_6, '10:00'), (TIME_7, '10:30'), (TIME_8, '11:00'),
                  (TIME_9, '11:30'), (TIME_10, '12:00'), (TIME_11, '12:30'), (TIME_12, '13:00'), (TIME_13, '13:30'), (TIME_14, '14:00'), (TIME_15, '14:30'),
                  (TIME_16, '15:00'), (TIME_17, '15:30'), (TIME_18, '16:00'), (TIME_19, '16:30'), (TIME_20, '17:00'), (TIME_21, '17:30'),
                  (TIME_22, '18:00'), (TIME_23, '18:30'), (TIME_24, '19:00')
]


class Boxtr(models.Model):
    

    id = models.BigAutoField(primary_key=True)
    flift = models.CharField(max_length=50, blank=True, null=True)
    truck = models.CharField(max_length=50, blank=True, null=True)
    arrival = models.CharField(max_length=50, blank=True, null=True, choices=ARRIVAL_CHOICES)
    pub_date = models.DateTimeField(blank=True, null=True)
    wet = models.CharField(max_length=50, blank=True, null=True, choices=WET_CHOICES, default='No')
    box1 = models.CharField(max_length=50, blank=True, null=True, choices=BOX_CHOICES)
    box1_qty = models.IntegerField(blank=True, null=True, choices=INTEGER_CHOICES)
    box2 = models.CharField(max_length=50, blank=True, null=True, choices=BOX_CHOICES)
    box2_qty = models.IntegerField(blank=True, null=True, choices=INTEGER_CHOICES)
    box3 = models.CharField(max_length=50, blank=True, null=True, choices=BOX_CHOICES)
    box3_qty = models.IntegerField(blank=True, null=True, choices=INTEGER_CHOICES)
    box4 = models.CharField(max_length=50, blank=True, null=True, choices=BOX_CHOICES)
    box4_qty = models.IntegerField(blank=True, null=True, choices=INTEGER_CHOICES)
    box5 = models.CharField(max_length=50, blank=True, null=True, choices=BOX_CHOICES)
    box5_qty = models.IntegerField(blank=True, null=True, choices=INTEGER_CHOICES)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'polls_boxtr'
 
 
 
        
class Boxtr_sum(models.Model):
 
    id = models.BigAutoField(primary_key=True)
    truck = models.CharField(max_length=50, blank=True, null=True)
    arrival = models.CharField(max_length=50, blank=True, null=True, choices=ARRIVAL_CHOICES)
    pub_date = models.DateTimeField(blank=True, null=True)
    wet = models.CharField(max_length=50, blank=True, null=True, choices=WET_CHOICES, default='No')
    box_qty = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'boxtr_sum'
