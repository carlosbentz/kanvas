from .views import ActivityView, CreateSubmissionView, RateSubmissionView, GetSubmissionView
from django.urls import path


urlpatterns = [
    path('activities/', ActivityView.as_view()),
    path('activities/<int:activity_id>/submissions/', CreateSubmissionView.as_view()), 
    path('submissions/<int:submission_id>/', RateSubmissionView.as_view()),
    path('submissions/', GetSubmissionView.as_view())
]
