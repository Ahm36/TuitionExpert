

from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=30,null=False,blank=False)
    description = models.TextField()

 

class Course(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False,blank=False)
    description = models.TextField()


class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=False,blank=False)
    

