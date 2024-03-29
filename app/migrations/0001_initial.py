# Generated by Django 2.2.6 on 2019-12-11 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='addresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=31, unique=True, verbose_name='address')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=31, unique=True, verbose_name='company')),
                ('year_of_foundation', models.DateField(blank=True, null=True, verbose_name='year_of_foundation')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=31, unique=True, verbose_name='country')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=31, verbose_name='department')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.addresses')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.companies')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'unique_together': {('department', 'company')},
            },
        ),
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name='name')),
                ('status', models.BooleanField(blank=True, null=True, verbose_name='status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.companies')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'unique_together': {('name', 'company')},
            },
        ),
        migrations.CreateModel(
            name='skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=31, unique=True, verbose_name='skill')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='specializations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=31, unique=True, verbose_name='specialization')),
            ],
            options={
                'verbose_name': 'Specialization',
                'verbose_name_plural': 'Specializations',
            },
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=31, verbose_name='task')),
                ('difficulty', models.IntegerField(blank=True, choices=[(1, 'Very easy'), (2, 'Easy'), (3, 'Normal'), (4, 'Hard'), (5, 'Very hard')], null=True, verbose_name='difficulty')),
                ('status', models.BooleanField(blank=True, null=True, verbose_name='status')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'unique_together': {('task', 'product')},
            },
        ),
        migrations.CreateModel(
            name='teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=31, verbose_name='team')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.departments')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'unique_together': {('team', 'department')},
            },
        ),
        migrations.CreateModel(
            name='employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, verbose_name='name')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='birthdate')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Man'), ('W', 'Woman')], max_length=1, null=True, verbose_name='gender')),
                ('experience', models.IntegerField(blank=True, default=0, null=True, verbose_name='experience')),
                ('salary', models.IntegerField(null=True, verbose_name='salary')),
                ('email', models.EmailField(blank=True, max_length=31, null=True, verbose_name='email')),
                ('confirmed', models.BooleanField(default=False, verbose_name='confirmed')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.addresses')),
                ('specialization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.specializations')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teams')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=31, verbose_name='city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.countries')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'unique_together': {('city', 'country')},
            },
        ),
        migrations.AddField(
            model_name='addresses',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cities'),
        ),
        migrations.CreateModel(
            name='team_tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tasks')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.teams')),
            ],
            options={
                'verbose_name': 'Team_task',
                'verbose_name_plural': 'Team_tasks',
                'unique_together': {('task', 'team')},
            },
        ),
        migrations.CreateModel(
            name='emploees_skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employees')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.skills')),
            ],
            options={
                'verbose_name': 'Emploees_skill',
                'verbose_name_plural': 'Emploees_skills',
                'unique_together': {('skill', 'employee')},
            },
        ),
    ]
