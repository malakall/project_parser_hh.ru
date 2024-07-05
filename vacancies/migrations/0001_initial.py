# Generated by Django 5.0.6 on 2024-07-05 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hh_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('salary_from', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_to', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('working_days', models.CharField(blank=True, max_length=255)),
                ('url', models.URLField()),
                ('address', models.TextField(blank=True, null=True)),
            ],
        ),
    ]