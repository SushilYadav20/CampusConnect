from django.urls import path
from .views import *

urlpatterns = [
    path('user-signup/',SignupView.as_view()),
    path('user-login/',LoginView.as_view()),
    path('user-logout/',LogoutView.as_view()),
    path('student-profile/',StudentProfileView.as_view()),
    path('faculty/',FacultyView.as_view()),
    path('department/',DepartmentView.as_view()),
    path('subject-list/',SubjectListView.as_view()),
    path('semester-view/',SemesterView.as_view()),
    path('assignment-view/',AssignmentView.as_view()),
    path('assignment-submission/',AssignmentSubmissionView.as_view()),
    path('attendance/',AttendanceView.as_view()),
         
]