import stripe

from config.settings import STRIPE_SECRET_KEY
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from courses.models import Course, Lesson, Payments, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.permissons import IsStaff, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer,\
    PaymentsSuccessSerializer, PaymentsRetrieveSerializer
from courses.tasks import send_mail_about_updating_course


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для Курса """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'update']:
            self.permission_classes = [IsAuthenticated, IsStaff | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsStaff | IsOwner]
        return super().get_permissions()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Контроллер создания Подписки """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Контроллер удаления Подписки """

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return response


class SubscriptionListAPIView(generics.ListAPIView):
    """ Контроллер вывода списка Подписок """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Контроллер создания Урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Если в Курс будет добавлен новый Урок, подписчикам этого курса будет отправлено уведомление"""

        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        send_mail_about_updating_course.delay(new_lesson.course.id)
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Контроллер вывода списка Уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Контроллер вывода информации по Уроку """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Контроллер изменения Урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsStaff]
    http_method_names = ['get', 'put', 'patch']


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Контроллер удаления Урока """

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    """ Контроллер вывода списка Платежей """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class PaymentsCreateAPIView(generics.CreateAPIView):
    """ Контроллер создания Платежей """

    serializer_class = PaymentsSerializer
    permission_classes = [AllowAny]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """ Контроллер вывода Платежа """

    serializer_class = PaymentsRetrieveSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny]


class PaymentSuccessAPIView(generics.RetrieveAPIView):
    stripe.api_key = STRIPE_SECRET_KEY
    serializer_class = PaymentsSuccessSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        session_id = self.request.query_params.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_id = session.metadata['payment_id']
        obj = get_object_or_404(self.get_queryset(), pk=payment_id)

        if not obj.is_paid:
            if session.payment_status == 'paid':
                obj.is_paid = True
                obj.save()
        return obj
