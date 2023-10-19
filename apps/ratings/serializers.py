from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    rater и agent - это дополнительные поля, которые вы добавили с использованием SerializerMethodField. 
    Эти поля определены методами get_rater и get_agent, которые определяют, каким образом значения этих полей должны быть 
    представлены в сериализованных данных.
    """
    rater = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)


    """
    Meta класс определяет мета-информацию для сериализатора.
    В данном случае, указывается модель Rating и исключаются 
    поля "update_at" и "pkid" из сериализации.
    """
    class Meta:
        model = Rating
        exclude = ["update_at", "pkid"]


    """
    Эти методы используются для получения значений полей rater и agent
    в сериализованных данных. Например, get_rater возвращает имя пользователя (username) для рейтинга.
    """
    def get_rater(self, obj):
        return obj.rater.username
    
    def get_agent(self, obj):
        return obj.agent.user.username


"""
Таким образом, этот сериализатор определяет, 
как объекты модели Rating должны быть представлены в виде данных JSON, 
и как обрабатывать эти данные при получении от клиента.
"""