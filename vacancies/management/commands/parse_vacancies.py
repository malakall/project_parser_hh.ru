import requests
from django.core.management.base import BaseCommand
from vacancies.models import Vacancy

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.management import call_command



class Command(BaseCommand):
    help = 'Parse vacancies from HH.ru and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--filter', type=str, help='Filter vacancies by name, salary or address')
        parser.add_argument('--value', type=str, help='Value for the filter')
        parser.add_argument('--pages', type=int, default=1, help='Number of pages to parse')

    def handle(self, *args, **options):
        def get_vacancies(filter_type, filter_value, pages=5):
            res = []
            for page in range(pages):
                params = {
                    'text': f'{filter_value}',
                    'page': page,
                    'per_page': 100,
                    'only_with_salary': 'true' if filter_type == 'salary' else 'false',
                }
                response = requests.get('https://api.hh.ru/vacancies/', params)
                req = response.json()
                if 'items' in req:
                    res.extend(req['items'])
                print(f"Page {page + 1} response: {len(req.get('items', []))} items")
                print('|', end='')
            return res

        filter_type = options['filter']
        filter_value = options['value']
        pages = options['pages']
        vacancies_data = get_vacancies(filter_type, filter_value, pages)

        if not vacancies_data:
            self.stdout.write(self.style.WARNING('No vacancies found.'))
            return

        for vac in vacancies_data:
            address = vac.get('address')
            if address:
                address = address.get('raw')
            Vacancy.objects.update_or_create(
                hh_id=vac['id'],
                defaults={
                    'name': vac['name'],
                    'salary_from': vac['salary']['from'] if vac['salary'] else None,
                    'salary_to': vac['salary']['to'] if vac['salary'] else None,
                    'working_days': vac['schedule']['name'] if 'schedule' in vac else '',
                    'url': vac['alternate_url'],
                    'address': address
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Data collected and filtered. Total vacancies: {len(vacancies_data)}'))



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
            vacancies = vacancies.filter(salary_from__lte=salary_to_filter)
        if address_filter:
            vacancies = vacancies.filter(address__icontains=address_filter)

        return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies})

    def post(self, request):
        pages = request.POST.get('pages', 1)
        call_command('parse_vacancies', pages=pages)
        return JsonResponse({'status': 'Database updated'})

class VacancyCountView(View):
    def get(self, request):
        count = Vacancy.objects.count()
        return JsonResponse({'count': count})