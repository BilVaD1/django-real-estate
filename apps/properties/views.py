import logging

import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PropertyNotFound
from .models import Property, PropertyViews
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,
                          PropertyViewSerializer)

logger = logging.getLogger(__name__)



"""
PropertyFilter - это класс фильтрации, созданный с использованием библиотеки 
django_filters в Django. Этот класс определяет, какие фильтры будут доступны 
для объектов модели Property при выполнении запросов.
"""
class PropertyFilter(django_filters.FilterSet):

    '''
    advert_type и property_type - это фильтры для точного 
    сравнения (без учета регистра) типов объявлений и типов недвижимости соответственно.
    '''
    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )

    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )

    price = django_filters.NumberFilter() #  это фильтр для точного сравнения цены.


    '''
    price__gt и price__lt - это фильтры для поиска объектов с ценой больше и меньше заданного значения соответственно.
    '''
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "price"] #  определяет, какие поля модели могут быть использованы для фильтрации.



# ListAllPropertiesAPIView это класс представления Django REST Framework, который предоставляет список всех объектов модели Property
class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at") # устанавливает базовый запрос для получения объектов модели. Здесь объекты упорядочены по дате создания в порядке убывания.
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, # for searching
        filters.OrderingFilter, # for sorting
    ]

    filterset_class = PropertyFilter # указывает класс фильтрации, который будет использоваться для фильтрации данных.
    search_fields = ["country", "city"] # определяет, по каким полям можно выполнять поиск.
    ordering_fields = ["created_at"] # определяет, по каким полям можно выполнять сортировку.





class ListAgentsPropertiesAPIView(generics.ListAPIView):

    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    '''
    get_queryset(self) - это метод, который возвращает набор данных, 
    который будет использоваться для создания ответа на запрос. 
    Здесь он возвращает все объекты Property, связанные с текущим пользователем 
    '''
    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by("-created_at") # отсортированные по дате создания в порядке убывания.
        return queryset


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all() # устанавливает базовый запрос для получения объектов модели. Здесь используется PropertyViews.objects.all(), что означает, что будут получены все объекты модели PropertyViews.


class PropertyDetailView(APIView):
    def get(self, request, slug):
        # Получаем объект Property по его slug
        property = Property.objects.get(slug=slug)

        # Получаем IP-адрес пользователя
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") # Здесь извлекается значение заголовка HTTP_X_FORWARDED_FOR из метаданных запроса, которые хранятся в атрибуте META объекта request.
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0] # Если x_forwarded_for существует, мы используем split(","), чтобы разделить строку на список, и затем берем первый элемент этого списка ([0]). Таким образом, ip теперь содержит первый IP-адрес из списка, который часто является оригинальным IP-адресом пользователя.
        else:
            ip = request.META.get("REMOTE_ADDR") # Если x_forwarded_for не существует (то есть запрос не проходил через прокси), мы используем request.META.get("REMOTE_ADDR") для получения оригинального IP-адреса пользователя, который был передан в заголовке REMOTE_ADDR.

        # Проверяем, существует ли запись о просмотре данного объекта Property с текущего IP-адреса
        if not PropertyViews.objects.filter(property=property, ip=ip).exists():
            # Если записи нет, создаем новую запись в PropertyViews
            PropertyViews.objects.create(property=property, ip=ip)

            # Увеличиваем счетчик просмотров объекта Property
            property.views += 1
            property.save() # сохраняют изменения в базе данных.

        # Создаем сериализатор и возвращаем детальную информацию о объекте Property
        serializer = PropertySerializer(property, context={"request": request}) # создает сериализатор для объекта Property, чтобы подготовить его к отправке в ответе.
        return Response(serializer.data, status=status.HTTP_200_OK)



'''
Этот код позволяет аутентифицированным пользователям обновлять информацию о 
своих объектах недвижимости с использованием HTTP-запроса типа PUT.
'''
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    try:
        # Например, если ваш URL выглядит как /update-property/my-cool-property/, то my-cool-property будет передано в качестве значения slug.
        property = Property.objects.get(slug=slug) # Slug - это короткая строка, предназначенная для использования в URL, которая обычно содержит только буквы, цифры, дефисы или подчеркивания
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user # Получение текущего пользователя из запроса.
    if property.user != user:
        return Response(
            {"error": "You can't update or edit a property that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data # Получение данных из тела запроса.
        serializer = PropertySerializer(property, data, many=False) # Создание экземпляра сериализатора (PropertySerializer) для объекта недвижимости с использованием полученных данных. many=False, потому что мы работаем с одним экземпляром недвижимости.
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = request.user
    data = request.data
    """
    поле user в модели Property представляет собой внешний ключ, 
    который связан с моделью пользователя. Добавление request.user.pkid в данные означает, 
    что создаваемый объект Property будет связан с конкретным пользователем, 
    который отправил запрос. 
    Это важно для отслеживания владельца каждого объекта Property в приложении.
    """
    data["user"] = request.user.pkid # добавляется информация о пользователе (user.pkid) в данные, которые будут переданы сериализатору
    serializer = PropertyCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"property {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user
    if property.user != user:
        return Response(
            {"error": "You can't delete a property that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = property.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)


@api_view(["POST"])
def uploadPropertyImage(request):
    data = request.data

    property_id = data["property_id"]
    property = Property.objects.get(id=property_id)
    property.cover_photo = request.FILES.get("cover_photo")
    property.photo1 = request.FILES.get("photo1")
    property.photo2 = request.FILES.get("photo2")
    property.photo3 = request.FILES.get("photo3")
    property.photo4 = request.FILES.get("photo4")
    property.save()
    return Response("Image(s) uploaded")




"""
PropertySearchAPIView представляет собой API-вид, 
предназначенный для выполнения поиска недвижимости на основе определенных параметров. 
"""
class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny] # означает, что к этому API-виду можно обращаться без аутентификации.
    serializer_class = PropertyCreateSerializer

    def post(self, request):
        queryset = Property.objects.filter(published_status=True)
        data = self.request.data

        """
        advert_type, property_type: Фильтрация по типу объявления и типу недвижимости.
        """
        advert_type = data["advert_type"]
        queryset = queryset.filter(advert_type__iexact=advert_type) # iexact обозначает "case-insensitive exact match". Это означает, что фильтрация будет осуществляться по точному соответствию значения поля property_type, но без учета регистра (большие и маленькие буквы не имеют значения).

        property_type = data["property_type"]
        queryset = queryset.filter(property_type__iexact=property_type)

        price = data["price"] # Фильтрация по цене, преобразование текстовых значений в числовые.
        if price == "$0+":
            price = 0
        elif price == "$50,000+":
            price = 50000
        elif price == "$100,000+":
            price = 100000
        elif price == "$200,000+":
            price = 200000
        elif price == "$400,000+":
            price = 400000
        elif price == "$600,000+":
            price = 600000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price) # __gte означает "greater than or equal to")

        bedrooms = data["bedrooms"] #  Фильтрация по количеству спален.
        if bedrooms == "0+":
            bedrooms = 0
        elif bedrooms == "1+":
            bedrooms = 1
        elif bedrooms == "2+":
            bedrooms = 2
        elif bedrooms == "3+":
            bedrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4
        elif bedrooms == "5+":
            bedrooms = 5

        queryset = queryset.filter(bedrooms__gte=bedrooms) # __gte означает "greater than or equal to")

        bathrooms = data["bathrooms"] #  Фильтрация по количеству ванных комнат.
        if bathrooms == "0+":
            bathrooms = 0.0
        elif bathrooms == "1+":
            bathrooms = 1.0
        elif bathrooms == "2+":
            bathrooms = 2.0
        elif bathrooms == "3+":
            bathrooms = 3.0
        elif bathrooms == "4+":
            bathrooms = 4.0

        queryset = queryset.filter(bathrooms__gte=bathrooms) # __gte означает "greater than or equal to")

        catch_phrase = data["catch_phrase"] # Фильтрация по фразе в описании.
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)

        return Response(serializer.data)
"""
Пример испеользования:

curl -X POST \
  http://example.com/api/property-search/ \
  -H 'Content-Type: application/json' \
  -d '{
    "advert_type": "For Sale",
    "property_type": "House",
    "price": "$100,000+",
    "bedrooms": "3+",
    "bathrooms": "2+",
    "catch_phrase": "spacious"
}'
"""
