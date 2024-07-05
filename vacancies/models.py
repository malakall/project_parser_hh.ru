from django.db import models

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    salary_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    working_days = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    address = models.TextField(null=True, blank=True)

    def str(self):
        return self.name