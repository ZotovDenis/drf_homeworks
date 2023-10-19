from rest_framework import serializers

from urllib.parse import urlparse


def validator_forbidden_urls(value):
    parsed_url = urlparse(value)
    if parsed_url.scheme == 'https' and parsed_url.netloc != 'www.youtube.com' or parsed_url.scheme == 'http':
        raise serializers.ValidationError('Запрещено использовать ссылки на видео с этой платформы!')
