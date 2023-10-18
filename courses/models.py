from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=120, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью курса', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец курса')
    price = models.IntegerField(verbose_name='Цена курса', default=10000)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    subscription = models.BooleanField(default=False, verbose_name='Подписка на обновления')

    def __str__(self):
        return f'{self.user} подписан на обновления курса {self.course}: {self.subscription}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Lesson(models.Model):
    title = models.CharField(max_length=120, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='course/lesson', verbose_name='Превью урока', **NULLABLE)
    video_url = models.URLField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец урока')
    price = models.IntegerField(verbose_name='Цена урока', default=1000)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    PAYMENT_CHOICES = (
        ('наличные', 'Наличные'),
        ('перевод на счет', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)

    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', **NULLABLE)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты', **NULLABLE)

    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')

    def __str__(self):
        return f'{self.user} оплатил {self.course if self.course else self.lesson}: ' \
               f'{self.payment_date} ({self.payment_method})'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
