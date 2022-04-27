from django.core.mail import send_mail
from .models import Team

def send_email_to_team_leader(team_id, from_email, task_name):
    """
        A email sending task 
    """
    leader = Team.objects.get(pk=team_id).leader                    # leader of Current team
    subject = 'New task assigned to your team'
    message = 'Hello {},\nHere is new task : {} assigned for your team please check it and refer the Manager for any query realated to it.'.format(leader.username, task_name)
    recipient_list = [leader.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)