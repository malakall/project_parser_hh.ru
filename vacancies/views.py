from django.shortcuts import render
from django.http import JsonResponse
from .models import Vacancy
from django.views import View
from django.core.management import call_command

class VacancyListView(View):
    def get(self, request):
        name_filter = request.GET.get('name')
        salary_from_filter = request.GET.get('salary_from')
        salary_to_filter = request.GET.get('salary_to')
        address_filter = request.GET.get('address')

        vacancies = Vacancy.objects.all()

        if name_filter:
            vacancies = vacancies.filter(name__icontains=name_filter)
        if salary_from_filter:
            vacancies = vacancies.filter(salary_from__gte=salary_from_filter)
        if salary_to_filter:
            vacancies = vacancies.filter(salary_to__lte=salary_to_filter)
        if address_filter:
            vacancies = vacancies.filter(address__icontains=address_filter)

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



    def post(self, request):
        pages = request.POST.get('pages', 1)
        call_command('parse_vacancies', pages=pages)
        return JsonResponse({'status': 'Database updated'})

