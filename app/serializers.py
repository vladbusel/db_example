from rest_framework import serializers
from app.models import *

class skillSerializer(serializers.ModelSerializer):
    class Meta:
        model = skills
        fields = '__all__'

class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = countries
        fields = '__all__'

class specializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = specializations
        fields = '__all__'

class companySerializer(serializers.ModelSerializer):

    class Meta:
        model = companies
        fields = '__all__'

class citySerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = cities
        fields = '__all__'

class addressSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = addresses
        fields = '__all__'

class departmentSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = departments
        fields = '__all__'

class teamSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    class Meta:
        model = teams
        fields = '__all__'

class team_taskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()
    team = serializers.StringRelatedField()

    class Meta:
        model = team_tasks
        fields = '__all__'

class taskSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = tasks
        fields = '__all__'

class productSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = products
        fields = '__all__'

class employeeSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    specialization = serializers.StringRelatedField()
    team = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = employees
        fields = '__all__'

class specialEmployeeSerializer(serializers.ModelSerializer):
    # specialization = serializers.StringRelatedField()
    # team = serializers.StringRelatedField()
    # address = serializers.StringRelatedField()

    class Meta:
        model = employees
        fields = ['name','birthdate','gender','specialization','team','address','experience','salary','email','confirmed']

class emploees_skillSerializer(serializers.ModelSerializer):
    skill = serializers.StringRelatedField()
    employee = serializers.StringRelatedField()

    class Meta:
        model = emploees_skills
        fields = '__all__'
