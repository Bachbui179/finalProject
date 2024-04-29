from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from application.models import Project, CustomUser, Student, Lecture
from django.contrib import messages
import math
from allocation_system.decorators import role_required

@login_required(login_url='/')
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
    
    return render(request, 'Admin/home.html', context)

@login_required(login_url='/')
@role_required(['1'])
def ADD_STUDENT(request):
    project = Project.objects.all()
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        project_id = request.POST.get('project_id')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,'Email Is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,'Username Is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,   
                user_type = 3,
                )
            
            user.set_password(password)
            user.save()

            project = Project.objects.get(id=project_id)

            student = Student(
                admin = user,
                project_assigned = project,
                gender = gender,
                )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Are Successfully Added !")
            return redirect('view_student')
    
    context = {
        'project': project,
    }
    return render(request, 'Admin/add_student.html', context)

@login_required(login_url='/')
@role_required(['1'])
def VIEW_STUDENT(request):
    student = Student.objects.all()
    
    context = {
        'student':student,
    }
    return render(request,'Admin/view_student.html', context)


@login_required(login_url='/')
@role_required(['1'])
def EDIT_STUDENT(request, id):
    student = Student.objects.select_related('admin', 'project_assigned').get(admin__id=id)
    student_firstname = student.admin.first_name
    student_lastname = student.admin.last_name
    student_id = student.admin.id
    student_email = student.admin.email
    username = student.admin.username
    project_assigned = student.project_assigned.name
    gender = student.gender
    project_assigned_id = Project.objects.get(name=project_assigned).id
    
    # Fetch all projects
    projects = Project.objects.all()
    
    context = {
        'student_id': student_id,
        'student_firstname': student_firstname,
        'student_lastname': student_lastname,
        'username': username,
        'student_email': student_email,
        'project_assigned': project_assigned,
        'projects': projects,
        'gender': gender,
        'project_assigned_id': project_assigned_id,
        
    }
    return render(request,'Admin/edit_student.html',context)

@login_required(login_url='/')
@role_required(['1'])
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        project_id = request.POST.get('project_id')

        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
                user.set_password(password)
        user.save()

        student = Student.objects.get(admin = student_id)
        student.gender = gender

        project = Project.objects.get(id = project_id)
        student.project_assigned = project

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'Admin/edit_student.html')

@login_required(login_url='/')
@role_required(['1'])
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_student')

@login_required(login_url='/')
@role_required(['1'])
def ADD_PROJECT(request):

    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('description')

        project = Project(
            name = project_name,
            description = project_description,
        )
        project.save()
        messages.success(request,'Project Are Successfully Created ')
        return redirect('view_project')
    
    context = {
        'project': Project,
    }
    return render(request, 'Admin/add_project.html', context)

@login_required(login_url='/')
@role_required(['1'])
def VIEW_PROJECT(request):
    project = Project.objects.all()
    
    context = {
        'project': project,
    }
    return render(request, 'Admin/view_project.html', context)

@login_required(login_url='/')
@role_required(['1'])
def EDIT_PROJECT(request, id):
    project = Project.objects.filter(id = id)
    
    context = {
        'project': project,
    }
    return render(request, 'Admin/edit_project.html', context)

@login_required(login_url='/')
@role_required(['1'])
def UPDATE_PROJECT(request):
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        project_id = request.POST.get('project_id')
        
        project = Project.objects.get(id = project_id)
        project.name = project_name
        project.description = description
        project.save()
        messages.success(request, "Project Updated Successfully!")
        
    return redirect('view_project')

@login_required(login_url='/')
@role_required(['1'])
def DELETE_PROJECT(request, id):
    project = Project.objects.get(id = id)
    project.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_project')

@login_required(login_url='/')
@role_required(['1'])
def ADD_LECTURE(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email Is Already Taken")
            return redirect('add_lecture')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username Is Already Taken')
            return redirect('add_lecture')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                user_type = 2,  
            )
            user.set_password(password)
            user.save()
            
            lecture = Lecture(
                admin = user,
                gender = gender,
            )
            lecture.save()
            messages.success(request, user.first_name + ' ' + user.last_name + 'Are Successfully Added !')
            return redirect('view_lecture')
        
    return render(request, 'Admin/add_lecture.html')


@login_required(login_url='/')
@role_required(['1'])
def VIEW_LECTURE(request):
    lecture = Lecture.objects.all()
    
    context = {
        'lecture': lecture
    }
    return render(request, 'Admin/view_lecture.html', context)

@login_required(login_url='/')
@role_required(['1'])
def EDIT_LECTURE(request, id):
    lecture = Lecture.objects.select_related('admin').get(admin__id=id)
    lecture_firstname = lecture.admin.first_name
    lecture_lastname = lecture.admin.last_name
    lecture_id = lecture.admin.id
    lecture_email = lecture.admin.email
    gender = lecture.gender
    username = lecture.admin.username
    
    context = {
        'lecture_id':lecture_id,
        'lecture_firstname': lecture_firstname,
        'lecture_lastname': lecture_lastname,
        'lecture_email': lecture_email,
        'gender': gender,
        'username': username,
    }
    return render(request,'Admin/edit_lecture.html',context)

@login_required(login_url='/')
@role_required(['1'])
def UPDATE_LECTURE(request):
    if request.method == "POST":
        lecture_id = request.POST.get('lecture_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = lecture_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
                user.set_password(password)
        user.save()

        lecture = Lecture.objects.get(admin = lecture_id)
        lecture.gender = gender

        lecture.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_lecture')

    return render(request,'Admin/edit_lecture.html')

@login_required(login_url='/')
@role_required(['1'])
def DELETE_LECTURE(request, admin):
    lecture = CustomUser.objects.get(id = admin)
    lecture.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_lecture')

@login_required(login_url='/')
@role_required(['1'])
def ALLOCATE(request):
    
    def stable_matching(students_preferences, teachers_preferences):
        max_students_per_teacher = math.ceil(len(students_preferences)/len(teachers_preferences))
        
        teachers_assigned = {teacher: [] for teacher in teachers_preferences}
        students_proposals = {student: 0 for student in students_preferences}
        proposals = {student: None for student in students_preferences}
        while None in proposals.values():
            for student in students_preferences:
                if proposals[student] is None:
                    teacher = students_preferences[student][students_proposals[student]]
                    if len(teachers_assigned[teacher]) < max_students_per_teacher:
                        teachers_assigned[teacher].append(student)
                        proposals[student] = teacher
                    else:
                        current_students = teachers_assigned[teacher]
                        current_students.sort(key=lambda x: teachers_preferences[teacher].index(x))
                        least_preferred_student = current_students.pop(0)
                        teachers_assigned[teacher].append(student)
                        proposals[student] = teacher
                        proposals[least_preferred_student] = None
                        students_proposals[least_preferred_student] += 1
                if None not in proposals.values():
                    break
        return proposals
    
    # Function to check if every user (except admin) has submitted their preference
    def check_preferences(data1, data2):
        message = 'All user submitted their preferences. Ready to allocate!'
        for user, preferences in data1.items():
            if len(preferences) != len(data2):
                message = f"User {user} has not submitted their preferences or preferences length mismatch."
                return False, message
            for preference in preferences:
                if preference not in data2:
                    message = "User {user} has an invalid preference: {preference}."
                    return False, message
                
        for user, preferences in data2.items():
            if len(preferences) != len(data1):
                message = f"User {user} has not submitted their preferences or preferences length mismatch."
                return False, message
            for preference in preferences:
                if preference not in data1:
                    message = "User {user} has an invalid preference: {preference}."
                    return False, message
                
        return True, message
    
    def find_name_by_email(email, email_dict):
        for name, email_address in email_dict.items():
            if email_address == email:
                return name
        return None
    
    lectures = Lecture.objects.all()
    students = Student.objects.all()
    
    student_info = {student.full_name: student.admin.email for student in students}
    lecture_info = {lecture.full_name: lecture.admin.email for lecture in lectures}
    user_info = {**student_info, **lecture_info}
    
    lectures_preference = {}
    for lecture in lectures:
        lectures_preference.update({lecture.admin.first_name + " " + lecture.admin.last_name: lecture.preference})
    
    # print(lectures_preference)
    
    students_preference = {}
    for student in students:
        students_preference.update({student.admin.first_name + " " + student.admin.last_name: student.preference})
    
    if check_preferences(students_preference, lectures_preference)[0] == True:
        if len(students_preference) == 0 or len(lectures_preference) ==0:
            messages.error(request, 'There are no students/lectures to allocate')
            context = {
            'status' : "Not Ready"
            }
            return render(request, 'Admin/allocate.html', context)
        else:
            name_match = (stable_matching(students_preference, lectures_preference))
            
            assigned_pairs_email = {student_info[student_name]: lecture_info[lecture_name] for student_name, lecture_name in name_match.items()}
            print(assigned_pairs_email)  
            for student_email, lecture_email in assigned_pairs_email.items():
            
                # Get the student instance corresponding to the email
                student = Student.objects.get(admin__email=student_email)
                
                # Get the lecture instance corresponding to the email
                lecture = Lecture.objects.get(admin__email=lecture_email)
                
                # assigned_lecture = lecture.full_name
                
                print(lecture)
                # Assign the lecture full name to the student
                student.lecture_assigned = lecture
                # print(student.lecture_assigned)
                student.save()
            
          
        
        messages.success(request, check_preferences(students_preference, lectures_preference)[1])
        context = {
            'status' : "Ready"
        }
        return render(request, 'Admin/allocate.html', context)
    else:
        
        messages.warning(request, check_preferences(students_preference, lectures_preference)[1])
        context = {
            'status' : "Not Ready"
        }
        return render(request, 'Admin/allocate.html', context)

@login_required(login_url='/')
@role_required(['1'])
def RESULT(request):
    students = Student.objects.all()

# Initialize an empty dictionary to store student data
    student_data = {}

    # Iterate through each student and populate the student_data dictionary
    for student in students:
        # Retrieve student full name
        full_name = student.full_name
        
        # Retrieve assigned lecture name
        assigned_lecture = student.lecture_assigned.full_name if student.lecture_assigned else None
        
        # Retrieve project assigned
        project_assigned = student.project_assigned.name if student.project_assigned else None
        
        # Populate student_data dictionary with student information
        student_data[full_name] = (assigned_lecture, project_assigned)
    context = {
        'student_data': student_data,
    }
    
    return render(request, 'Admin/result.html', context)