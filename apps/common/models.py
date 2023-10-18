from django.db import models
import uuid

class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False) # Поле для первичного ключа с типом BigAutoField. Это большое целочисленное поле с автоматическим инкрементом.
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
    Meta класс с abstract = True делает эту модель абстрактной. 
    Абстрактные модели не создают таблицы в базе данных, они предназначены для использования как базовые классы для других моделей. 
    Другие модели могут наследоваться от TimeStampedUUIDModel и использовать ее поля, добавляя свои собственные.
    """
    class Meta:
        abstract = True
