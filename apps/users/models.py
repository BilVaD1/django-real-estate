import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManage

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False) # оле для первичного ключа с типом BigAutoField. Это большое целочисленное поле с автоматическим инкрементом.
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Поле для уникального идентификатора пользователя типа UUIDField. Уникальный идентификатор генерируется автоматически с использованием uuid.uuid4().
    username = models.CharField(verbose_name=_('Username'), max_length=255, unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=50)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) # Поле, отражающее дату и времени присоединения пользователя.

    '''
    USERNAME_FIELD и REQUIRED_FIELDS: Определение поля, которое будет использоваться в качестве уникального идентификатора пользователя (в данном случае, email). REQUIRED_FIELDS - это список полей, которые требуются для создания пользователя.
    '''
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[ 'username', 'first_name', 'last_name']

    objects = CustomUserManage() # Менеджер пользователей, определенный в CustomUserManager (предполагается, что он определен в файле managers.py).

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username # Возвращает строковое представление пользователя, в данном случае - его имя пользователя.
    

    '''
    get_full_name и get_short_name методы: Предоставляют полное и короткое имя пользователя соответственно.
    '''
    @property
    def get_full_name(self):
        return f'{self.first_name.title()} {self.last_name.title()}'
    
    def get_short_name(self):
        return self.username




