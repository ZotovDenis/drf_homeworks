from celery import shared_task
from django.core.mail import send_mail

from config import settings
from courses.models import Subscription


@shared_task
def send_mail_about_updating_course(course_id):
    course_subscribers = Subscription.objects.filter(course=course_id)
    for sub in course_subscribers:
        send_mail(
            subject=f'Обновление по курсу {sub.course.title}!',
            message=f'Курс {sub.course.title} был обновлён!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f'{sub.user.email}'],
            fail_silently=True
        )
    print('Уведомления об обновлении курса отправлены.')
