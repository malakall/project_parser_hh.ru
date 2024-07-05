from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('vacancies:list', permanent=True)),  # Перенаправление на страницу с вакансиями
    path('vacancies/', include('vacancies.urls')),
]