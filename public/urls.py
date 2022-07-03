from django.urls import path
from . import views


urlpatterns = [

    path('',views.index,name='index'),
    path('expert_register/',views.expert_register,name='expert-register'),
    path('student_register/',views.student_register,name='student-register'),
    path('login/',views.login_page,name='login'),
    path('student_home/',views.student_home,name='student-home'),
    path('subject_experts/<str:pk>/',views.subject_experts,name='subject-experts'),
    path('student_expert_request/<str:pk>/',views.student_expert_request,name='student-exp-req'),
    path('expert_home/',views.expert_home,name='expert-home'),
    path('createclassroom/<str:pk>/',views.create_classroom,name='create-classroom'),
    path('expertclassrooms/',views.expert_classrooms,name='expert-classrooms'),
    path('expertclassroom/<str:pk>/',views.expert_classroom,name='expert-classroom'),
    path('notesuploadform/<str:pk>/',views.upload_notes,name='upload-notes'),
    path('videouploadform/<str:pk>/',views.upload_videos,name='upload-videos'),
    path('taskuploadform/<str:pk>/',views.upload_tasks,name='upload-tasks'),
    path('viewqueries/<str:pk>/',views.view_queries,name='view-queries'),
    path('studentclassrooms/',views.student_classrooms,name='student-classrooms'),
    path('studentclassroom/<str:pk>/',views.student_classroom,name='student-classroom'),
    path('viewnotes/<str:pk>/',views.view_notes,name='view-notes'),
    path('logoutstudent',views.logout_student,name='logout-student'),
    path('viewvideos/<str:pk>/',views.view_videos,name='view-videos'),
    path('viewtasks/<str:pk>/',views.view_tasks,name='view-tasks'),
    path('uploadanswer/<str:pk>/',views.upload_answer,name='upload-answer'),
    path('makequery/<str:pk>/',views.make_query,name='make-query'),
    path('logoutexpert',views.logout_expert,name='logout-expert'),
    path('logoutadmin',views.logout_admin,name='logout-admin'),
]


