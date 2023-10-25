from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile

from .models import Rating

User = get_user_model()

# create agent review
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    print(profile_id)
    print( Profile.objects.all() )
    agent_profile = Profile.objects.get(id=profile_id, is_agent=True) # Получает профиль агента по его идентификатору (profile_id). Ожидается, что профиль существует и является профилем агента.
    data = request.data # Получаются данные из тела запроса

    profile_user = User.objects.get(pkid=agent_profile.user.pkid)
    if profile_user.email == request.user.email:
        formatted_response = {"message": "You can't rate yourself"}
        return Response(formatted_response, status=status.HTTP_403_FORBIDDEN)



    """
    Здесь происходит фильтрация отзывов, связанных с текущим профилем агента 
    (agent_profile). agent__pkid означает, что мы фильтруем по полю agent в 
    связанных отзывах, и это поле представляет собой внешний ключ, указывающий на 
    профиль агента. profile_user.pkid - это идентификатор пользователя, 
    оставляющего отзыв. Таким образом, мы ищем отзывы, где агент совпадает 
    с agent_profile, и оценивающий пользователь совпадает с profile_user.
    """
    alreadyExists = agent_profile.agent_review.filter(
        agent__pkid=profile_user.pkid
    ).exists() # Метод exists() возвращает булево значение (True или False), указывающее на то, существуют ли отзывы, которые соответствуют критериям фильтрации. 

    if alreadyExists:
        formatted_response = {"detail": "Profile already reviewed"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    elif data["rating"] == 0:
        formatted_response = {"detail": "Please select a rating"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Создание нового объекта Rating в базе данных.
        review = Rating.objects.create(
            rater=request.user,
            agent=agent_profile,
            rating=data["rating"],
            comment=data["comment"],
        )
        reviews = agent_profile.agent_review.all() # Получение всех отзывов, связанных с профилем агента (agent_profile).
        agent_profile.num_reviews = len(reviews) #  Обновление поля num_reviews в профиле агента, указывающего на количество отзывов.

        total = 0 # Инициализация переменной total для хранения суммы всех оценок.
        for i in reviews:
            total += i.rating # Проход по всем отзывам и суммирование их оценок.
 
        agent_profile.rating = round(total / len(reviews), 2) # Расчет средней оценки на основе имеющихся отзывов. 
        agent_profile.save() # Сохранение обновленных данных профиля агента в базе данных.
        return Response("Review Added")
