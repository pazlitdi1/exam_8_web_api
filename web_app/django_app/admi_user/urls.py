from django.urls import path
from .views import UserAdminView, RegisterAdminView, LoginAdminView

urlpatterns = [
    path('', UserAdminView.as_view(), name='user-admin'),
    path('login-admin/', LoginAdminView.as_view(), name='login-admin'),
    path('register-admin/', RegisterAdminView.as_view(), name='register-admin'),
]
