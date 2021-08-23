from .views import SignupView, LoginView
from django.urls import path


urlpatterns = [
    path('accounts/', SignupView.as_view()),
    path('login/', LoginView.as_view())
]
