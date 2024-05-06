from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from application.models import Project, CustomUser, Student, Lecture
from allocation_system.decorators import role_required

@role_required(['2'])
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
    return render(request, 'Lecture/home.html', context)

@role_required(['2'])
def VIEW_STUDENT(request):
    student = Student.objects.all()
    
    context = {
        'student': student
    }
    return render(request ,'Lecture/view_student.html', context)

@login_required(login_url='/')
@role_required(['2'])
def VIEW_PROJECT(request):
    project = Project.objects.all()
    
    context = {
        'project': project
    }
    return render(request, 'Lecture/view_project.html', context)

@role_required(['2'])
def SUBMIT_PREFERENCE(request):
    student = Student.objects.all()
    student_count = Student.objects.all().count()
    
    
    if request.method == "POST":
        # Get the list of selected preferences
        preferences = request.POST.getlist('preferences')
        student_name = request.POST.getlist('student_name')
        
        
        def has_duplicates(arr):
            seen = set()
            for item in arr:
                if item in seen:
                    return True
                seen.add(item)
            return False

        if has_duplicates(preferences) == True:
            messages.error(request, 'Students can not have the same position!')
            return redirect('submit_preference')
        else: 
            sorted_combined = sorted(
                list(zip(preferences, student_name)), 
                key=lambda x: int(x[0])
                )
            submit_preference = [lecture for _, lecture in sorted_combined]
            lecture = Lecture.objects.get(admin=request.user)
            
            lecture.preference = submit_preference
            messages.success(request,'Submissions completed')
            lecture.save()
            
    context = {
        'student': student,
        'student_count': student_count,
        'n' : range(student_count),
        }
    
    return render(request, 'Lecture/submit_preference.html', context)

@role_required(['2'])
def ASSIGNED(request):
    lecture = Lecture.objects.get(admin=request.user)
    
    content = {
       'students_assigned': students_assigned,
    }
    
    students_assigned = Student.objects.filter(lecture_assigned=lecture)
    if students_assigned == []:
        messages.error(request,'No student(s) assigned yet! Please wait until administrator start allocation process!')
        return render(request, 'view_assigned.html')
    else:
        return render(request, 'Lecture/view_assigned.html', content)