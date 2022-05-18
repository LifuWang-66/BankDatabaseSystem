from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.urls import reverse


cursor = connection.cursor()

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {"form": form}
    return render(request, "accounts/register.html", context)

# Create your views here.
def login_view(request):
    # future -> ?next=/articles/create/
    if request.method == "POST":
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     login(request, user)
        #     return redirect('../bank')
        username = request.POST.get("username")
        password = request.POST.get("password")
        # no sql injection possibility :P
        query = "select * from person where perID = '" + username + "' and pwd = '" + password + "'"
        cursor.execute(query)
        result = cursor.fetchall()
        if (len(result) == 1):
            # return redirect(reverse('app:view', kwargs={ 'username': username }))
            request.session['username'] = username
            return redirect('../../bank')
        else:
            messages.error(request, "Wrong username or password. Please try again!")
            return render(request, "accounts/login.html")
    else:
        # form = AuthenticationForm(request)
        return render(request, "accounts/login.html", {})


def logout_view(request):
    request.session['username'] = ''
    return redirect('../../bank')
