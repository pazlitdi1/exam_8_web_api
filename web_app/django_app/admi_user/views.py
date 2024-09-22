from django.contrib import messages
from django.shortcuts import render
import requests
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect


class UserAdminView(View):
    def get(self, request):
        return render(request, 'index_admin.html')


class LoginAdminView(View):
    def get(self, request):
        return render(request, 'auth/login_admin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        url = "http://127.0.0.2:8007/admin/login/"
        data = {
            "username": username,
            "password": password,
        }

        if username and password:
            response = requests.post(url, json=data)
            if response.json()["status_code"] == 200:
                access_token = response.json()['access_token']

                response = redirect('index_admin')
                response.set_cookie('access_token', access_token, httponly=True)  # Tokenni cookie'da saqlash
                return response
            else:
                messages.error(request, "Invalid login credentials")

        return render(request, 'auth/login_admin.html')


class RegisterAdminView(View):
    def get(self, request):
        return render(request, 'auth/register_admin.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        url = "http://127.0.0.2:8007/admin/register/"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password,
        }

        if all([first_name, last_name, username, email, phone, password]):
            response = requests.post(url, json=data)
            try:
                response.raise_for_status()  # Raise an error for bad responses
                detail = response.json().get('detail')

                if detail == "email":
                    messages.error(request, 'Email already exists.')
                elif detail == "username":
                    messages.error(request, 'Username already exists.')
                else:
                    return redirect('auth/login_admin')
                # Render the registration page with the error message
            except requests.exceptions.HTTPError:
                error_message = "username yoki email alloqachon ro`yxatdan o`tgan"
                return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
            except (ValueError, KeyError):
                error_message = "Error processing FastAPI response."
                return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
        else:
            error_message = 'All fields are required.'
            return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
from django.shortcuts import render

# Create your views here.
