from .base import *

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend" # This line is telling Django to use Celery for sending emails in the background. Instead of sending emails synchronously during the request-response cycle, which could introduce delays, Celery allows you to offload the email sending task to a separate process.
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = 'info@real-estate.com'
DOMAIN = env('DOMAIN')
SITE_NAME = 'Real Estate'

DATABASES = {
    'default':{
        'ENGINE': env("POSTGRESS_ENGINE"),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('PG_HOST'),
        'PORT': env('PG_PORT')
    }
}



"""
CSRF_TRUSTED_ORIGINS is a setting introduced in Django 3.1 to enhance security related to Cross-Site Request Forgery (CSRF) protection. 
CSRF is an attack where a malicious website can make a user's browser perform an unwanted action on a different site where the user is authenticated.

In the context of Django, when a POST request is made to the server, Django checks the origin of the request to prevent CSRF attacks. 
If the origin of the request doesn't match any trusted origins, Django rejects the request.
"""
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']

CELERY_BROKER_URL = env("CELERY_BROKER")
CELERY_RESULT_BACKEND = env("CELERY_BACKEND")
CELERY_TIMEZONE = "Africa/Kigali"


