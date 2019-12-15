from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class countries(models.Model):
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    country = models.CharField(verbose_name='country',max_length=31,unique=True)

    def __str__(self):
        template = '{0.country}'
        return template.format(self)

class CountriesForm(ModelForm):
    class Meta:
        model = countries
        fields = ['country']


class cities(models.Model):
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ('city', 'country',)

    city = models.CharField(verbose_name='city', max_length=31)
    country = models.ForeignKey(countries, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.city}'
        return template.format(self)

class CitiesForm(ModelForm):
    class Meta:
        model = cities
        fields = ['city','country']


class addresses(models.Model):
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    address = models.CharField(verbose_name='address',max_length=31,unique=True)
    city = models.ForeignKey(cities, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.address}'
        return template.format(self)

class AddressesForm(ModelForm):
    class Meta:
        model = addresses
        fields = ['address','city']


class companies(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    company = models.CharField(verbose_name='company',max_length=31,unique=True)
    year_of_foundation = models.DateField(verbose_name='year_of_foundation', blank=True, null=True)

    def __str__(self):
        template = '{0.company}'
        return template.format(self)

class CompaniesForm(ModelForm):
    class Meta:
        model = companies
        fields = ['company','year_of_foundation']


class departments(models.Model):
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        unique_together = ('department', 'company',)

    department = models.CharField(verbose_name='department',max_length=31)
    company = models.ForeignKey(companies, on_delete=models.CASCADE)
    address = models.ForeignKey(addresses, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.department}'
        return template.format(self)

class DepartmentsForm(ModelForm):
    class Meta:
        model = departments
        fields = ['department','company', 'address']


class teams(models.Model):
    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        unique_together = ('team', 'department',)

    team = models.CharField(verbose_name='team',max_length=31)
    department = models.ForeignKey(departments, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.team}'
        return template.format(self)

class TeamsForm(ModelForm):
    class Meta:
        model = teams
        fields = ['team','department']


class specializations(models.Model):
    class Meta:
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"

    specialization = models.CharField(verbose_name='specialization',max_length=31,unique=True)

    def __str__(self):
        template = '{0.specialization}'
        return template.format(self)

class SpecializationsForm(ModelForm):
    class Meta:
        model = specializations
        fields = ['specialization']


class products(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        unique_together = ('name', 'company',)

    name = models.CharField(verbose_name='name',max_length=31)
    company = models.ForeignKey(companies, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='status', blank=True, null=True)

    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class ProductsForm(ModelForm):
    class Meta:
        model = products
        fields = ['name','company','status']


class tasks(models.Model):
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = ('task', 'product',)

    DIFFICULTY = (
    (1, 'Very easy'),
    (2, 'Easy'),
    (3, 'Normal'),
    (4, 'Hard'),
    (5, 'Very hard'),
    )
    task = models.CharField(verbose_name='task',max_length=31)
    difficulty = models.IntegerField(verbose_name='difficulty', choices=DIFFICULTY, blank=True, null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='status', blank=True, null=True)

    def __str__(self):
        template = '{0.task}'
        return template.format(self)

class TasksForm(ModelForm):
    class Meta:
        model = tasks
        fields = ['task','difficulty','product','status']


class team_tasks(models.Model):
    class Meta:
        verbose_name = "Team_task"
        verbose_name_plural = "Team_tasks"
        unique_together = ('task', 'team',)

    task = models.ForeignKey(tasks, on_delete=models.CASCADE)
    team = models.ForeignKey(teams, on_delete=models.CASCADE)


    def __str__(self):
        template = '{0.task} {0.team}'
        return template.format(self)

class Team_tasksForm(ModelForm):
    class Meta:
        model = team_tasks
        fields = ['task','team']

class employees(models.Model):
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    GENDERS = (
    ('M', 'Man'),
    ('W', 'Woman'),
    )
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='name',max_length=31)
    birthdate = models.DateField(verbose_name='birthdate', blank=True, null=True)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDERS, blank=True, null=True)
    specialization =  models.ForeignKey(specializations, on_delete=models.CASCADE, blank=True, null=True)
    team =  models.ForeignKey(teams, on_delete=models.CASCADE, blank=True, null=True)
    address =  models.ForeignKey(addresses, on_delete=models.CASCADE, blank=True, null=True)
    experience = models.IntegerField(verbose_name='experience', default = 0, blank=True, null=True)
    salary = models.IntegerField(verbose_name='salary', null=True)
    email = models.EmailField(verbose_name='email', max_length=31, blank=True, null=True)
    confirmed = models.BooleanField(verbose_name='confirmed', default=False)

    def __str__(self):
        template = '{0.username}'
        return template.format(self)

class EmployeesForm(ModelForm):
    class Meta:
        model = employees
        fields = '__all__'

class skills(models.Model):
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    skill = models.CharField(verbose_name='skill',max_length=31,unique=True)

    def __str__(self):
        template = '{0.skill}'
        return template.format(self)

class SkillsForm(ModelForm):
    class Meta:
        model = skills
        fields = ['skill']

class emploees_skills(models.Model):
    class Meta:
        verbose_name = "Emploees_skill"
        verbose_name_plural = "Emploees_skills"
        unique_together = ('skill', 'employee',)

    skill = models.ForeignKey(skills, on_delete=models.CASCADE)
    employee = models.ForeignKey(employees, on_delete=models.CASCADE)

    def __str__(self):
        template = '{0.skill} {0.employee}'
        return template.format(self)

class Emploees_skillsForm(ModelForm):
    class Meta:
        model = emploees_skills
        fields = ['skill','employee']
