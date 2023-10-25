from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from real_estate.settings.development import DEFAULT_FROM_EMAIL

from .models import Enquiry


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def send_enquiry_email(request):
    data = request.data # Получение данных из тела POST-запроса.

    try:
        # Извлечение значений полей (темы, имени, электронной почты, сообщения) из данных запроса.
        subject = data["subject"]
        name = data["name"]
        email = data["email"]
        message = data["message"]
        from_email = data["email"] # Использование электронной почты отправителя в качестве адреса отправителя письма.
        recipient_list = [DEFAULT_FROM_EMAIL] #  Список получателей письма. Здесь используется глобальная переменная DEFAULT_FROM_EMAIL, которая, вероятно, содержит адрес, указанный в настройках Django как адрес "по умолчанию" для исходящих писем.

        send_mail(subject, message, from_email, recipient_list, fail_silently=True) # Функция Django для отправки электронных писем

        enquiry = Enquiry(name=name, email=email, subject=subject, message=message) # Создание объекта модели Enquiry
        enquiry.save()

        return Response({"success": "Your Enquiry was successfully submitted"})

    except:
        return Response({"fail": "Enquiry was not sent. Please try again"})
