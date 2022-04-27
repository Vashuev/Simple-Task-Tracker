from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    user_roles = (
        ('U', 'user'),
        ('L', 'Team Leader'),
        ('M', 'Team Member'),
    )

    role = models.CharField(choices=user_roles, max_length=1, default='M')

class Team(models.Model):

    name = models.CharField(max_length=200)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name='leader')
    members = models.ManyToManyField(CustomUser, related_name='members')

    def clean(self):
        if self.leader.role != 'L':
            raise ValidationError(_('user is not team-leader'))
        if self.members.role != 'M':
            raise ValidationError(_('user is not team-member'))
    
    def __str__(self):
        return self.name


class Task(models.Model):
    status_choice = (
        ('A', 'Assigned'),
        ('I', 'In progress'),
        ('U', 'Under Review'),
        ('D', 'Done'),
    )

    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    status = models.CharField(choices=status_choice, max_length=1, default='A')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

