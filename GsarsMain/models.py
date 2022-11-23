from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.
# class Admin(models.Model):
#     firstName = models.CharField(max_length=30)
#     middleName = models.CharField(max_length=30)
#     lastName = models.CharField(max_length=30)
#     email= models.CharField(max_length=35)
#     password= models.CharField(max_length=255)

class Students(models.Model):
    SID = models.IntegerField(primary_key = True)
    firstName = models.CharField(max_length=30)
    middleName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30)
    email = models.CharField(max_length=35, unique=False)
    password = models.CharField(max_length=255, unique=False, default='ChangeYourPassword')
    programme = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    semester = models.CharField(max_length=50)
    sl =  models.IntegerField(default=1)
    role = models.CharField(max_length=50)
#     adminID = models.ForeignKey(Admin,on_delete=models.CASCADE)

# class Focal(models.Model):
#     firstName = models.CharField(max_length=30)
#     middleName = models.CharField(max_length=30)
#     lastName = models.CharField(max_length=30)
#     email= models.CharField(max_length=35)
#     password= models.CharField(max_length=255)
#     designation= models.CharField(max_length=35)
#     role= models.CharField(max_length=35)
#     adminID = models.ForeignKey(Admin, on_delete=models.CASCADE)

# class ActivityRecord(models.Model):
#     aName =  models.CharField(max_length=50)
#     category = models.CharField(max_length=50)
#     year = models.IntegerField()
#     Semester = models.CharField(max_length=50)
#     date = models.DateField()
#     fID = models.ForeignKey(Focal, on_delete=models.CASCADE)

# class Record(models.Model):
#     sID = models.ForeignKey(Students, on_delete=models.CASCADE)
#     aID = models.ForeignKey(ActivityRecord, on_delete=models.CASCADE)
#     status = models.CharField(max_length=35)


