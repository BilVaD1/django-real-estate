from .base import *

DATABASES = {
    'default':{
        'ENGINE': env("POSTGRESS_ENGINE"),
        'NAME': env('POSTGRES_DB'),
        'USER':env('POSTGRES_USERNAME'),
        'PASSWORD':env('POSTGRES_PASSWORD'),
        'HOST':env('PG_HOST'),
        'PORT':env('PG_PORT')
    }
}

