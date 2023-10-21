import json

from rest_framework.renderers import JSONRenderer

'''
Этот класс представляет собой кастомный JSON-рендерер, 
который можно использовать в Django REST Framework для
форматирования ответов в JSON.
'''
class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    # Этот метод переопределяет метод render базового класса JSONRenderer.
    '''
    Входные параметры:

    data: данные, которые будут отрендерены.
    accepted_media_types: список поддерживаемых типов медиа.
    renderer_context: контекст рендеринга.

    В методе сначала проверяется наличие ошибок в данных. 
    Если ошибки есть, то просто используется базовый рендерер. 
    В противном случае данные оборачиваются в словарь с ключом "profile" 
    и затем преобразуются в JSON.
    '''
    def render(self, data, accepted_media_types=None, renderer_context=None):
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)

        return json.dumps({"profile": data})
