import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'dudoan.html', {})


def ketqua(request):
    return render(request, 'ketqua.html', {})
