from rest_framework import serializers

from courses.models import Course, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lessons', many=True)

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lesson_count(instance):
        if instance.lessons.all().count():
            return instance.lessons.all().count()
        return 0


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'
