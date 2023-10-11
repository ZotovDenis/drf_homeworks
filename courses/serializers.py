from rest_framework import serializers

from courses.models import Course, Lesson, Payments, Subscription
from courses.validators import validator_forbidden_urls


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validator_forbidden_urls], required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lessons', many=True)
    description = serializers.CharField(validators=[validator_forbidden_urls])
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lesson_count(instance):
        """ Подсчет количества уроков в курсе """
        if instance.lessons.all().count():
            return instance.lessons.all().count()
        return 0

    def get_is_subscribed(self, obj):
        """ Включаем информацию о подписке текущего пользователя на курс """
        user = self.context['request'].user
        try:
            subscription = Subscription.objects.get(user=user, course=obj)
            return subscription.subscription
        except Subscription.DoesNotExist:
            return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
