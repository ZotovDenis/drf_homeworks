from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from courses.serializers import SubscriptionSerializer
from users.models import User


class LessonListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")
        self.lesson = Lesson.objects.create(title="lesson_test", course=self.course, owner=self.user)

    def test_get_list(self):
        """ Тест получения списка уроков """

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "video_url": self.lesson.video_url,
                        "description": self.lesson.description,
                        "title": self.lesson.title,
                        "preview": self.lesson.preview,
                        "course": self.lesson.course_id,
                        "owner": self.lesson.owner_id
                    }
                ]
            }
        )


class LessonCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")

    def test_lesson_create(self):
        """ Тест создания урока """

        self.client.force_authenticate(user=self.user)
        data = {'title': 'lesson_test_2', 'course': self.course.id}

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": response.json()["id"],
                "video_url": None,
                "description": None,
                "title": "lesson_test_2",
                "preview": None,
                "course": self.course.id,
                "owner": None
            }
        )

    def test_lesson_create_validation_error(self):
        """ Тест создания урока с запрещенной ссылкой """

        self.client.force_authenticate(user=self.user)
        data = {'title': 'lesson_test_2', 'course': self.course.id, 'video_url': 'https://example.com'}

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'video_url': ['Запрещено использовать ссылки на видео с этой платформы!']})


class LessonUpdateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")
        self.lesson = Lesson.objects.create(title='lesson_test', owner=self.user, course=self.course,
                                            video_url='https://www.youtube.com/video=000',
                                            description='Test description')

    def test_lesson_update(self):
        """ Тест изменения урока """

        self.client.force_authenticate(user=self.user)
        url = f'/lesson/update/{self.lesson.id}/'
        data = {
            'title': 'updated_lesson',
            'video_url': 'https://www.youtube.com/video=001',
            'description': 'Updated description'
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'updated_lesson')
        self.assertEqual(self.lesson.video_url, 'https://www.youtube.com/video=001')
        self.assertEqual(self.lesson.description, 'Updated description')

    def test_lesson_update_validation_error(self):
        """ Тест изменения урока с запрещенной ссылкой """

        self.client.force_authenticate(user=self.user)
        url = f'/lesson/update/{self.lesson.id}/'
        data = {'video_url': 'http://www.youtube.com/video=001'}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'video_url': ['Запрещено использовать ссылки на видео с этой платформы!']})


class LessonRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")
        self.lesson = Lesson.objects.create(title='lesson_test', owner=self.user, course=self.course,
                                            video_url='https://www.youtube.com/video=000',
                                            description='Test description')

    def test_lesson_retrieve(self):
        """ Тест просмотра урока """

        self.client.force_authenticate(user=self.user)
        url = f'/lesson/{self.lesson.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve_wrong_user(self):
        """ Тест запрета на просмотр урока, если пользователь - не владелец """

        user = User.objects.create(email='wronguser@example.com', password='fake1password')
        self.client.force_authenticate(user=user)
        url = f'/lesson/{self.lesson.id}/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")
        self.lesson = Lesson.objects.create(title='lesson_test', owner=self.user, course=self.course,
                                            video_url='https://www.youtube.com/video=000',
                                            description='Test description')

    def test_delete_lesson(self):
        """ Тест удаления урока """

        self.client.force_authenticate(user=self.user)
        url = f'/lesson/delete/{self.lesson.id}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_wrong_user(self):
        """ Тест запрета на удаление урока, если пользователь - не владелец """

        user = User.objects.create(email='wronguser@example.com', password='fake1password')
        self.client.force_authenticate(user=user)
        url = f'/lesson/delete/{self.lesson.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', password='test123password')
        self.course = Course.objects.create(title="course_test")

    def test_create_subscription(self):
        """ Тест создания подписки """

        self.client.force_authenticate(user=self.user)
        url = '/subscription/create/'
        data = {
            'user': self.user.id,
            'course': self.course.id,
            'subscription': True
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        subscription = Subscription.objects.get()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertEqual(subscription.subscription, True)

    def test_delete_subscription(self):
        """ Тест удаления подписки """

        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course, subscription=True)
        url = f'/subscription/delete/{self.subscription.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_list_subscriptions(self):
        """ Тест списка подписок """

        self.client.force_authenticate(user=self.user)
        url = '/subscriptions/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscriptions = Subscription.objects.filter(user=self.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        self.assertEqual(response.data, serializer.data)
