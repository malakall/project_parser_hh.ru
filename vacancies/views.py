from django.shortcuts import render
from django.http import JsonResponse
from .models import Vacancy
from django.views import View
from django.core.management import call_command

class VacancyListView(View):
    def get(self, request):
        filter_type = request.GET.get('filter')
        filter_value = request.GET.get('value')
        vacancies = Vacancy.objects.all()

        if filter_type and filter_value:
            if filter_type == 'name':
                vacancies = vacancies.filter(name__icontains=filter_value)
            elif filter_type == 'salary':
                vacancies = vacancies.filter(salary_from__gte=filter_value)
            elif filter_type == 'address':
                vacancies = vacancies.filter(address__icontains=filter_value)

        return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})

    def post(self, request):
        filter_type = request.POST.get('filter')
        filter_value = request.POST.get('value')
        pages = request.POST.get('pages', 1)
        call_command('parse_vacancies', filter=filter_type, value=filter_value, pages=pages)
        return JsonResponse({'status': 'Database updated'})

class VacancyCountView(View):
    def get(self, request):
        count = Vacancy.objects.count()
        return JsonResponse({'count': count})
    


def count_vacancies(request):
    filter_type = request.GET.get('filter')
    filter_value = request.GET.get('value')

    vacancies = Vacancy.objects.all()

    if filter_type == 'name' and filter_value:
        vacancies = vacancies.filter(name__icontains=filter_value)
    elif filter_type == 'salary' and filter_value:
        vacancies = vacancies.filter(salary_from__gte=filter_value)
    elif filter_type == 'address' and filter_value:
        vacancies = vacancies.filter(address__icontains=filter_value)

    count = vacancies.count()
    return JsonResponse({'count': count})