from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', obtain_auth_token, name='login'),  
    path('upload/', views.upload_assignment, name='upload'),
    path('admins/', views.get_admins, name='get_admins'),
    path('assignments/', views.view_assignments, name='view_assignments'),
    path('assignments/<int:id>/accept/', views.accept_assignment, name='accept_assignment'),
    path('assignments/<int:id>/reject/', views.reject_assignment, name='reject_assignment'),
]

