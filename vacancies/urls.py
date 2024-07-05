from django.urls import path
from .views import VacancyListView, VacancyCountView

app_name = 'vacancies'

urlpatterns = [
    path('', VacancyListView.as_view(), name='list'),
    path('upload/', VacancyListView.as_view(), name='upload'),
    path('count/', VacancyCountView.as_view(), name='count'),
]