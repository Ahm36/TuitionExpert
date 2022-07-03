
from unicodedata import category
from django.db import models
from main.models import Subject,Category,Course

# Create your models here.


class LoginT(models.Model):
    USER_TYPE=[
        ('A','Admin'),
        ('E','Expert'),
        ('S','Student'),
    ]
    username=models.CharField(max_length=30,null=False,blank=False)
    password= models.CharField(max_length=30,null=False,blank=False)
    type = models.CharField(max_length=1,choices=USER_TYPE)

class Expert(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Others'),
    ]
    STATUS=[
        ('W','Waiting'),
        ('A','Approved'),
        ('R','Rejected'),
        ('B','Blocked'),
    ]
    name = models.CharField(max_length=30,null=False,blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    qualification = models.CharField(max_length=30)
    details = models.TextField()
    experience = models.IntegerField()
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    status = models.CharField(max_length=1,choices=STATUS)


class ExpertDocument(models.Model):
    expert =  models.ForeignKey(Expert,on_delete=models.CASCADE)
    document_name = models.CharField(max_length=30)
    file = models.FileField(upload_to='expdoc')
    details = models.TextField()


class Student(models.Model):
    name = models.CharField(max_length=40)
    place = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100,null=True,blank=True)


class StudentRequest(models.Model):
    REQ_STATUS=[
        ('W','Waiting'),
        ('A','Approved'),
        ('R','Rejected'),
    ]
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert,on_delete=models.CASCADE)
    req_date = models.DateTimeField()
    allot_date = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=1,choices=REQ_STATUS)


class Classroom(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert,on_delete=models.CASCADE)


class Notes(models.Model):
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to='notes')
    description = models.TextField()

class Video(models.Model):
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to='videos')
    description = models.TextField()

class Task(models.Model):
    TASK_STATUS=[
        ('W','Waiting'),
        ('V','Verified'),
        ('R','Resubmit'),
    ]
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    question = models.CharField(max_length=30)
    task_file = models.FileField(upload_to='tasks')
    answer_file = models.FileField(upload_to='tasks',null=True,blank=True)
    description = models.TextField()
    status=models.CharField(max_length=1,choices=TASK_STATUS,null=True,blank=True)

class Queries(models.Model):
    QUERY_STAT=[
        ('W','Waiting'),
        ('A','Answered'),      
    ]
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    query = models.CharField(max_length=90)
    answer = models.CharField(max_length=90,null=True)
    status = models.CharField(max_length=1,choices=QUERY_STAT,null=True,blank=True)
    date = models.DateTimeField(auto_now=True)