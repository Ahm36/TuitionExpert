from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.admin_home,name='admin-home'),
    path('addcategory',views.add_category,name='add-category'),
    path('viewcategory',views.view_category,name='view-category'),
    path('removecategory/<str:pk>/',views.remove_category,name='remove-category'),
    path('addcourse',views.add_course,name='add-course'),
    path('viewcourse',views.view_course,name='view-course'),
    path('removecourse/<str:pk>/',views.remove_course,name='remove-course'),
    path('addsubject',views.add_subject,name='add-subject'),
    path('viewsubjects',views.view_subjects,name='view-subjects'),
    path('removesubject/<str:pk>/',views.remove_subject,name='remove-subject'),
    path('expertrequests',views.expert_requests,name='expert-requests'),
    path('approveexpert/<str:pk>/',views.approve_expert,name='approve-expert'),
    path('rejectexpert/<str:pk>/',views.reject_expert,name='reject-expert'),
    path('blockexpert/<str:pk>/',views.block_expert,name='block-expert'),
    path('unblockexpert/<str:pk>/',views.unblock_expert,name='unblock-expert'),
    path('expertrequests',views.expert_requests,name='expert-requests'),
    path('studentrequests',views.student_requests,name='student-requests'),
    path('approvesreq/<str:pk>/',views.approve_sreq,name='approve-sreq'),
    path('rejectsreq/<str:pk>/',views.reject_sreq,name='reject-sreq'),
    

]
