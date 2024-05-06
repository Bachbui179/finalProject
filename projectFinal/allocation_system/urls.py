from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import Lecture_views, views, Admin_views, Student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name = 'base'),
    
    # Login path
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='doLogout'),
    
    #Admin path
    path('Admin/Home', Admin_views.HOME, name='admin_home'),
    
    #Profile Update
    path('Profile/', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    
    #Admin path/Student
    path('Admin/Student/Add', Admin_views.ADD_STUDENT, name='add_student'),
    path('Admin/Student/View', Admin_views.VIEW_STUDENT, name = 'view_student'),
    path('Admin/Student/Edit/<str:id>', Admin_views.EDIT_STUDENT, name = 'edit_student'),
    path('Admin/Student/Delete<str:admin>', Admin_views.DELETE_STUDENT, name = 'delete_student'),
    path('Admin/Student/Update', Admin_views.UPDATE_STUDENT, name = 'update_student'),
    
    #Admin path/Project
    path('Admin/Project/Add', Admin_views.ADD_PROJECT, name = 'add_project'),
    path('Admin/Project/View', Admin_views.VIEW_PROJECT, name = 'view_project'),
    path('Admin/Project/Edit/<str:id>', Admin_views.EDIT_PROJECT, name = 'edit_project'),
    path('Admin/Project/Delete/<str:id>', Admin_views.DELETE_PROJECT, name = 'delete_project'),
    path('Admin/Project/Update', Admin_views.UPDATE_PROJECT, name = 'update_project'),
    
    #Admin path/Lecture
    path('Admin/Lecture/Add', Admin_views.ADD_LECTURE, name = 'add_lecture'),
    path('Admin/Lecture/View', Admin_views.VIEW_LECTURE, name = 'view_lecture'),
    path('Admin/Lecture/Edit/<str:id>', Admin_views.EDIT_LECTURE, name = 'edit_lecture'),
    path('Admin/Lecture/Delete/<str:id>', Admin_views.DELETE_LECTURE, name = 'delete_lecture'),
    path('Admin/Lecture/Update', Admin_views.UPDATE_LECTURE, name = 'update_lecture'),
    
    #Admin path/Allocate
    path('Admin/Allocate', Admin_views.ALLOCATE, name = 'allocate_process'),
    path('Admin/Result', Admin_views.RESULT, name = 'result'),
    
    #Lecture path/
    path('Lecture/Home', Lecture_views.HOME, name='lecture_home'),
    path('Lecture/Student/View', Lecture_views.VIEW_STUDENT,name='lecture_view_student'),
    path('Lecture/Project/View', Lecture_views.VIEW_PROJECT, name = 'lecture_view_project'),
    path('Lecture/SubmitForm', Lecture_views.SUBMIT_PREFERENCE, name = 'submit_preference'),
    path('Lecture/Assigned', Lecture_views.ASSIGNED, name = 'lecture_view_assigned'),
    
    #Student path/
    path('Student/Home', Student_views.HOME, name='student_home'),
    path('Student/Lecture/View', Student_views.VIEW_LECTURE, name = 'student_view_lecture'),
    path('Student/Project/View', Student_views.VIEW_PROJECT, name = 'student_view_project'),
    path('Student/SubmitForm', Student_views.SUBMIT_PREFERENCE, name = 'student_submit_preference'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'allocation_system.views.error_404'