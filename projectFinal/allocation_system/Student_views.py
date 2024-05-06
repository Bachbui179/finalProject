from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from application.models import Project, CustomUser, Student, Lecture
from allocation_system.decorators import role_required
from django.contrib.auth.decorators import *

@login_required(login_url='/')
@role_required(['3'])
def HOME(request):
    student_count = Student.objects.all().count()
    lecture_count = Lecture.objects.all().count()
    project_count = Project.objects.all().count()
    
    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()
    
    context = {
        'student_count': student_count,
        'lecture_count': lecture_count,
        'project_count': project_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }
    return render(request, 'Student/home.html', context)

@login_required(login_url='/')
@role_required(['3'])
def VIEW_LECTURE(request):
    lecture = Lecture.objects.all()
    
    context = {
        'lecture': lecture
    }
    return render(request ,'Student/view_lecture.html', context)

@login_required(login_url='/')
@role_required(['3'])
def VIEW_PROJECT(request):
    project = Project.objects.all()
    
    context = {
        'project': project
    }
    return render(request, 'Student/view_project.html', context)

@login_required(login_url='/')
@role_required(['3'])
def SUBMIT_PREFERENCE(request):
    lecture = Lecture.objects.all()
    lecture_count = Lecture.objects.all().count()
    
    if request.method == "POST":
        # Get the list of selected preferences
        preferences = request.POST.getlist('preferences')
        lecture_name = request.POST.getlist('lecture_name')
        
        def has_duplicates(arr):
            seen = set()
            for item in arr:
                if item in seen:
                    return True
                seen.add(item)
            return False

        if has_duplicates(preferences) == True:
            messages.error(request, 'Lectures can not have the same position!')
            return redirect('student_submit_preference')
        else: 
            sorted_combined = sorted(
                list(zip(preferences, lecture_name)), 
                key=lambda x: int(x[0])
                )
            submit_preference = [lecture for _, lecture in sorted_combined]
            student = Student.objects.get(admin=request.user)
            student.preference = submit_preference
            student.save()
        
    context = {
        'lecture': lecture,
        'lecture_count': lecture_count,
        'n' : range(lecture_count),
        }
    
    return render(request, 'Student/submit_preference.html', context)

@role_required(['3'])
def ASSIGNED(request):
    student = Student.objects.get(admin=request.user)
    assigned_lecture = Lecture.objects.get(admin__username=student.lecture_assigned)
    content = {
        'assigned_lecture': assigned_lecture,
    }
    if assigned_lecture == []:
        messages.error(request,'No lecture assigned yet! Please wait until administrator start allocation process!')
        return render(request, 'Student/student_view_assigned.html')
    else:
        return render(request, 'Student/student_view_assigned.html',content)