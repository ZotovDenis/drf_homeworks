from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'description', 'preview')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('owner', )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'owner', 'description', 'preview', 'video_url')
    search_fields = ('title', 'description', 'owner')
    list_filter = ('owner', 'course')
