from .views import SignupView, LoginView, ProtectedView
from django.urls import path

urlpatterns = [
    path('accounts/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('protected/', ProtectedView.as_view()),
]
