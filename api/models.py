from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  
        blank=True,
    )

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_admin')
    created_at = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'), 
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected')
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.task}"
