from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from app.serializers import *
from app.models import *
from rest_framework import status
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes #renderer_classes
from django.db import IntegrityError, transaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from db_project.forms import UserRegistrationForm
from app.permissions import *


@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_user_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/users/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "username,password\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["username"] = fields[0]
                data_dict["password"] = fields[1]
                data_dict["password2"] = fields[1]
                data_dict["first_name"] = ''
                data_dict["email"] = ''
                try:
                    form = UserRegistrationForm(data_dict)
                    if len(User.objects.filter(username = data_dict["username"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                with transaction.atomic():
                    for form in forms:
                        new_user = form.save(commit=False)
                        new_user.set_password(form.cleaned_data['password'])
                        new_user.save()
            except IntegrityError:
                handle_exception()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_country_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/countries/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "country\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["country"] = fields[0]
                try:
                    form = CountriesForm(data_dict)
                    if len(countries.objects.filter(country = fields[0][0:-1])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                with transaction.atomic():
                    for form in forms:
                        form.save()
            except IntegrityError:
                handle_exception()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_city_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/cities/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "city,country\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["city"] = fields[0]
                data_dict["country"] = countries.objects.get(country=fields[1][0:-1]).id
                try:
                    form = CitiesForm(data_dict)
                    if len(cities.objects.filter(city=data_dict["city"],country=data_dict["country"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                with transaction.atomic():
                    for form in forms:
                        form.save()
            except IntegrityError:
                handle_exception()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_address_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/addresses/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "address,city\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["address"] = fields[0]
                data_dict["city"] = cities.objects.get(city=fields[1][0:-1]).id
                try:
                    form = AddressesForm(data_dict)
                    if len(addresses.objects.filter(address=data_dict["address"],city=data_dict["city"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                with transaction.atomic():
                    for form in forms:
                        form.save()
            except IntegrityError:
                handle_exception()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_company_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/companies/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "company,year_of_foundation\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["company"] = fields[0]
                data_dict["year_of_foundation"] = fields[1][0:-1]
                try:
                    form = CompaniesForm(data_dict)
                    if len(companies.objects.filter(company=data_dict["company"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                with transaction.atomic():
                    for form in forms:
                        form.save()
            except IntegrityError:
                handle_exception()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_department_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/departments/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "department,company,address\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["department"] = fields[0]
                data_dict["company"] = companies.objects.get(company=fields[1]).id
                data_dict["address"] = addresses.objects.get(address=fields[2][0:-1]).id
                try:
                    form = DepartmentsForm(data_dict)
                    if len(departments.objects.filter(department=data_dict["department"],company=data_dict["company"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_team_csv(request):
    data = {}
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/teams/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "team,department\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["team"] = fields[0]
                data_dict["department"] = departments.objects.get(department=fields[1][0:-1]).id
                try:
                    form = TeamsForm(data_dict)
                    if len(teams.objects.filter(team=data_dict["team"],department=data_dict["department"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_specialization_csv(request):
    data = {}
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/specializations/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "specialization\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["specialization"] = fields[0]
                try:
                    form = SpecializationsForm(data_dict)
                    if len(specializations.objects.filter(specialization=data_dict["specialization"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_product_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/products/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "name,company,status\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["name"] = fields[0]
                data_dict["company"] = companies.objects.get(company=fields[1]).id
                data_dict["status"] = fields[2][0:-1]
                try:
                    form = ProductsForm(data_dict)
                    if len(products.objects.filter(name=data_dict["name"],company=data_dict["company"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_task_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/tasks/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "task,difficulty,product,status\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["task"] = fields[0]
                data_dict["difficulty"] = fields[1]
                data_dict["product"] = products.objects.get(name=fields[2]).id
                data_dict["status"] = fields[3][0:-1]
                try:
                    form = TasksForm(data_dict)
                    if len(tasks.objects.filter(task=data_dict["task"], product=data_dict["product"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_team_task_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/team_tasks/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "task,team\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["task"] = tasks.objects.get(task=fields[0]).id
                data_dict["team"] = teams.objects.get(team=fields[1][0:-1]).id
                try:
                    form = Team_tasksForm(data_dict)
                    if len(team_tasks.objects.filter(task=data_dict["task"],team=data_dict["team"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_employee_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/employees/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "username,name,birthdate,gender,specialization,team,address,experience,salary,email\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["username"] = User.objects.get(username=fields[0]).id
                data_dict["name"] = fields[1]
                data_dict["birthdate"] = fields[2]
                data_dict["gender"] = fields[3]
                data_dict["specialization"] = specializations.objects.get(specialization=fields[4]).id
                data_dict["team"] = teams.objects.get(team=fields[5]).id
                data_dict["address"] = addresses.objects.get(address=fields[6]).id
                data_dict["experience"] = fields[7]
                data_dict["salary"] = fields[8]
                data_dict["email"] = fields[9][0:-1]
                data_dict["confirmed"] = 0
                try:
                    form = EmployeesForm(data_dict)
                    if len(employees.objects.filter(username=data_dict["username"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_skill_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/skills/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):

            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        #if file is too large, return
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "skill\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["skill"] = fields[0]
                try:
                    form = SkillsForm(data_dict)
                    if len(skills.objects.filter(skill=data_dict["skill"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated,))
@api_view(('GET','POST'))
@transaction.atomic
def upload_employees_skill_csv(request):
    if "GET" == request.method:
        data = {"url" : "http://127.0.0.1:8000/api/app/upload/csv/employees_skills/"}
        return render(request, "app/upload_csv.html", context = data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return Response({"error': 'Uploaded file isn't csv format."},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        if csv_file.multiple_chunks():
            return Response({'error': 'Uploaded file is too big.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[0:-1]
        forms = []
        header = lines[0]
        lines = lines[1:len(lines)]
        if header == "skill,employee\r":
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["skill"] = skills.objects.get(skill=fields[0]).id
                data_dict["employee"] = employees.objects.get(username=User.objects.get(username=fields[1][0:-1]).id).id
                print(data_dict)
                try:
                    form = Emploees_skillsForm(data_dict)
                    if len(emploees_skills.objects.filter(skill=data_dict["skill"], employee=data_dict["employee"])) == 0:
                        if form.is_valid():
                            forms.append(form)
                        else:
                            return Response({'error': "Uploaded file isn't valid."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                except:
                    return Response({'error': "Files form isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            for form in forms:
                form.save()
        else:
            return Response({'error': "Files header isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

class CountriesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  countries.objects.all()
        serializer = countrySerializer(queryset, many=True)
        return Response({'countries': serializer.data},status=status.HTTP_200_OK)

class CitiesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  cities.objects.all()
        serializer = citySerializer(queryset, many=True)
        return Response({'cities': serializer.data},status=status.HTTP_200_OK)

class AddressesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  addresses.objects.all()
        serializer = addressSerializer(queryset, many=True)
        return Response({'addresses': serializer.data},status=status.HTTP_200_OK)

class CompaniesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  companies.objects.all()
        serializer = companySerializer(queryset, many=True)
        return Response({'companies': serializer.data},status=status.HTTP_200_OK)

class DepartmentsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  departments.objects.all()
        serializer = departmentSerializer(queryset, many=True)
        return Response({'departments': serializer.data},status=status.HTTP_200_OK)

class TeamsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  teams.objects.all()
        serializer = teamSerializer(queryset, many=True)
        return Response({'teams': serializer.data},status=status.HTTP_200_OK)

class SpecializationsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  tasks.objects.all()
        serializer = taskSerializer(queryset, many=True)
        return Response({'tasks': serializer.data},status=status.HTTP_200_OK)

class ProductsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  products.objects.all()
        serializer = productSerializer(queryset, many=True)
        return Response({'products': serializer.data},status=status.HTTP_200_OK)

class TasksListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  tasks.objects.all()
        serializer = taskSerializer(queryset, many=True)
        return Response({'tasks': serializer.data},status=status.HTTP_200_OK)

class Team_tasksListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  team_tasks.objects.all()
        serializer = team_taskSerializer(queryset, many=True)
        return Response({'team_tasks': serializer.data},status=status.HTTP_200_OK)

class EmployeesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  employees.objects.all()
        serializer = employeeSerializer(queryset, many=True)
        return Response({'employees': serializer.data},status=status.HTTP_200_OK)

class ConfirmedEmployeesListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  employees.objects.filter(confirmed=True)
        serializer = employeeSerializer(queryset, many=True)
        return Response({'confirmed_employees': serializer.data},status=status.HTTP_200_OK)

class SkillsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  skills.objects.all()
        serializer = skillSerializer(queryset, many=True)
        return Response({'skills': serializer.data},status=status.HTTP_200_OK)

class Employees_skillsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset =  emploees_skills.objects.all()
        serializer = emploees_skillSerializer(queryset, many=True)
        return Response({'employees_skills': serializer.data},status=status.HTTP_200_OK)

class CountryView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = countrySerializer
    queryset = countries.objects.all()

class AddCountryView(generics.CreateAPIView):
    serializer_class = countrySerializer

class CityView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = citySerializer
    queryset = cities.objects.all()

class AddAddressView(generics.CreateAPIView):
    serializer_class = addressSerializer

class AddressView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = addressSerializer
    queryset = addresses.objects.all()

class AddCityView(generics.CreateAPIView):
    serializer_class = citySerializer

class CompanyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = companySerializer
    queryset = companies.objects.all()

class AddCompanyView(generics.CreateAPIView):
    serializer_class = companySerializer

class DepartmentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = departmentSerializer
    queryset = departments.objects.all()

class AddDepartmentView(generics.CreateAPIView):
    serializer_class = departmentSerializer

class TeamView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = teamSerializer
    queryset = teams.objects.all()

class AddTeamView(generics.CreateAPIView):
    serializer_class = teamSerializer

class SpecializationView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = specializationSerializer
    queryset = specializations.objects.all()

class AddSpecializationView(generics.CreateAPIView):
    serializer_class = specializationSerializer

class ProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = productSerializer
    queryset = products.objects.all()

class AddProductView(generics.CreateAPIView):
    serializer_class = productSerializer

class TaskView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = taskSerializer
    queryset = tasks.objects.all()

class AddTaskView(generics.CreateAPIView):
    serializer_class = taskSerializer

class EmployeeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = specialEmployeeSerializer
    queryset = employees.objects.all()

    def get_object(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            return employees.objects.get(id=pk)
        except employees.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object_dict(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            return employees.objects.in_bulk([pk])
        except employees.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        employee = self.get_object(pk)
        serializer = employeeSerializer(employee)
        return Response({'employee': serializer.data},status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        employee = self.get_object_dict(request).get(pk)
        if request.user == employee.username or request.user.is_staff:
            data = request.data
            data_dict = {}
            data_dict["username"] = employee.username
            data_dict["name"] = employee.name if data.get('name','') == '' else data.get('name')
            data_dict["birthdate"] = employee.birthdate if data.get('birthdate','') == '' else data.get('birthdate')
            data_dict["gender"] = employee.gender if data.get('gender','') == '' else data.get('gender')
            data_dict["specialization"] = employee.specialization if data.get('specialization','') == '' else specializations.objects.get(id=data.get('specialization'))
            data_dict["team"] = employee.team if data.get('team','') == '' else teams.objects.get(id=data.get('team'))
            data_dict["address"] = employee.address if data.get('address','') == '' else addresses.objects.get(id=data.get('address'))
            data_dict["experience"] = employee.experience if data.get('experience','') == '' else data.get('experience')
            data_dict["salary"] = employee.salary if data.get('salary','') == '' else data.get('salary')
            data_dict["email"] = employee.email if data.get('email','') == '' else data.get('email')
            changed = (data_dict["name"] != employee.name) or (data_dict["birthdate"] != employee.birthdate) or (data_dict["birthdate"] != employee.birthdate) or (data_dict["gender"] != employee.gender) or (data_dict["specialization"] != employee.specialization)  or (data_dict["team"] != employee.team) or (data_dict["address"] != employee.address) or (data_dict["experience"] != employee.experience) or (data_dict["salary"] != employee.salary) or (data_dict["email"] != employee.email)
            data_dict["confirmed"] = employee.confirmed if (request.user.is_staff==0 and changed==0) else False if request.user.is_staff==0 else (data.get('confirmed',False) == 'true')
            try:
                employees.objects.update_or_create(id=pk, defaults = data_dict)
                serializer = employeeSerializer(employees.objects.get(id=pk))
            except:
                return Response({'error': "Data isn't correct."},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AddEmployeeView(generics.CreateAPIView):
    serializer_class = specialEmployeeSerializer

class SkillView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = skillSerializer
    queryset = skills.objects.all()

class AddSkillView(generics.CreateAPIView):
    serializer_class = skillSerializer

class Emploees_skillView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = emploees_skillSerializer
    queryset = emploees_skills.objects.all()

class AddEmploees_skillView(generics.CreateAPIView):
    serializer_class = emploees_skillSerializer

# class AddManyCountriesView(APIView):
#
#     def post(self, request):
#         number = int(request.data.get('number'))
#         l = len(countries.objects.all())
#         for i in range(number):
#             l += 1
#             country = countries(country='Country#'+str(l))
#             country.save()
#         serializer = countrySerializer(countries.objects.all()[l-int(number):l], many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
