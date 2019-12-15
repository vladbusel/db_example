from db_project.forms import UserRegistrationForm
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(('GET','POST'))
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            return Response(status=status.HTTP_200_OK)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})
