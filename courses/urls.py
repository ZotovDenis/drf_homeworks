from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonUpdateAPIView, LessonListAPIView, \
    LessonRetrieveAPIView, LessonDestroyAPIView, PaymentsListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, SubscriptionListAPIView, PaymentsCreateAPIView, PaymentSuccessAPIView, \
    PaymentsRetrieveAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

                  path('payments/', PaymentsListAPIView.as_view(), name='payment_list'),
                  path('payments/create/', PaymentsCreateAPIView.as_view(), name='payment_create'),
                  path('payments/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='payments_detail'),
                  path('payments/success/', PaymentSuccessAPIView.as_view(), name='payments_success'),

                  path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription_list'),
                  path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
                  path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(),
                       name='subscription_delete'),

              ] + router.urls
