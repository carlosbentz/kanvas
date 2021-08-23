from .views import CourseView, RetrieveCourseView, CourseEnrollView
from django.urls import path


urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:course_id>/', RetrieveCourseView.as_view()),
    path('courses/<int:course_id>/registrations/', CourseEnrollView.as_view()) 
]
