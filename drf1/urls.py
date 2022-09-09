from turtle import title
from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from . import views

from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'students', views.StudentsViewSet)
urlpatterns = routers.urls

urlpatterns = [
    # path('', views.students, name ='students'),
    path('lists/', views.model_student, name ='list_students'),
    path('lists/<int:pk>/', views.student_detail, name ='list_students'),
    path('all_stu/', views.StudentList.as_view(), name ='all_students'),
    path('all_stu/<int:pk>/', views.StudentDetail.as_view(), name ='student'),
    path('all_stu_generic/', views.StudentGenericList.as_view(), name ='all_students'),
    path('all_stu_generic/<int:pk>/', views.SetudentGenericDetail.as_view(), name ='all_students'),

    #using APIview
    path('student_create/', views.StudentCreateView.as_view(), name='studen_create'),
    path('student_delete/<int:id>/', views.StudentDestroy.as_view(), name='student_destroy'),
    path('all_stu/student/<int:id>/', views.StudentRetriveUpdateDestroy.as_view(), name='student_destroy'),

    # using classed based views
    path('create_student/', views.CreateStudent.as_view(), name='create_student'),

    # schema view
    path('swagger_docs/', get_swagger_view(title="Student API")),

]

urlpatterns = format_suffix_patterns(urlpatterns)