from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class UserModels(UserAdmin):
    list_display = ['id', 'first_name', 'last_name','username', 'user_type', 'email', 'get_preference']
    
    def get_preference(self, obj):
        if obj.user_type == '2':
            lecture = obj.lecture
            return lecture.preference if lecture else None
        elif obj.user_type == '3':
            student = obj.student
            return student.preference if student else None
        else:
            return None
    get_preference.short_description = 'preference'
  
@admin.register(Project)  
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'project_assigned','lecture_assigned', 'get_email', 'preference', 'updated_at')
    
    def get_username(self, obj):
        return obj.admin.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.admin.email
    get_email.short_description = 'Email'
    
    
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ( 'get_username', 'gender', 'get_email','get_students', 'preference', 'updated_at')
    
    def get_username(self, obj):
        return obj.admin.username
    get_username.short_description = 'Username'
    
    def get_email(self, obj):
        return obj.admin.email
    get_email.short_description = 'Email'
    
    def get_students(self, obj):
        return ", ".join([student.admin.username for student in obj.students.all()])
    get_students.short_description = 'student(s) assigned'