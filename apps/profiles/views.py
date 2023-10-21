from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer



'''
При GET-запросе, если пользователь аутентифицирован, 
он получит список профилей агентов в формате JSON.
'''
class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated] # указывает, что для доступа к этому представлению пользователь должен быть аутентифицирован.
    queryset = Profile.objects.filter(is_agent=True) # определяет, какие объекты будут включены в список агентов. В данном случае, выбираются профили, у которых is_agent равно True.
    serializer_class = ProfileSerializer #  указывает, какой сериализатор будет использоваться для сериализации данных.


"""
    from rest_framework import api_view, permissions

    @api_view(["GET"])
    @permission_classes((permissions.IsAuthenticated))
    def get_all_agents(request):
        agents = Profile.objects.filter(is_agent=True)
        serializer=ProfileSerializer(agents, many=True)
        name_spaced_response={"agents": serializer.data}
        return Response(name_spaced_response,status=status.HTTP_200_OK)
"""


class TopAgentsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer



"""
Это представление предназначено для получения профиля пользователя и 
возврата данных профиля в формате JSON.
"""
class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer] #  указывает, что для форматирования ответа будет использоваться кастомный JSON-рендерер ProfileJSONRenderer.

    def get(self, request):
        user = self.request.user # получает текущего аутентифицированного пользователя.
        user_profile = Profile.objects.get(user=user) # получает профиль пользователя.
        serializer = ProfileSerializer(user_profile, context={"request": request}) # создает экземпляр сериализатора ProfileSerializer для сериализации данных профиля. 
        #print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK) #  возвращает сериализованные данные профиля в ответе с кодом статуса 200 (OK).


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    serializer_class = UpdateProfileSerializer

    # username берется из URL
    def patch(self, request, username):
        """
        Эта запись связана с моделью данных. Вероятно, в модели Profile есть поле user, 
        которое является внешним ключом к модели User. И чтобы получить профиль пользователя по его имени (username), 
        используется двойное подчеркивание __, что является синтаксисом для выполнения связанных запросов в Django ORM.

        Таким образом, строка Profile.objects.get(user__username=username) ищет профиль, 
        которого поле user соответствует пользователю с определенным именем (username). 
        В данном случае, вероятно, происходит проверка существования профиля пользователя перед его обновлением.
        """
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        user_name = request.user.username # получает имя пользователя, отправившего запрос.
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True # Параметр partial=True позволяет обновлять только указанные поля.
        ) 

        serializer.is_valid() #  проверяет валидность данных.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) #  возвращает сериализованные данные профиля в ответе с кодом статуса 200 (OK).
