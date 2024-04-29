from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    USER = (
		('1','ADMIN'),
		('2','LECTURE'),
		('3','STUDENT'))
    user_type = models.CharField(choices=USER, max_length=50, default = 1)
    preference = models.JSONField(default=list, blank=True, null=True)
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name   
    
class Lecture(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preference = models.JSONField(default=list, blank= True)

    @property
    def full_name(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

    def __str__(self):
        return self.admin.username
    
class Student(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=100)
    project_assigned = models.ForeignKey(Project, on_delete=models.DO_NOTHING, default=None, blank=True)
    lecture_assigned = models.ForeignKey(Lecture, on_delete=models.DO_NOTHING, null=True, related_name='students', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preference = models.JSONField(default=list, blank=True)
    
    @property
    def full_name(self):
        return f"{self.admin.first_name} {self.admin.last_name}"
    
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name