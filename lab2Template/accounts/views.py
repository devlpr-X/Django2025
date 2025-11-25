from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account
from .forms import RegisterForm, AccountForm, UserUpdateForm, AccountUpdateForm

def user_register(request):
    if request.method == "POST":
        r_form = RegisterForm(request.POST)
        a_form = AccountForm(request.POST, request.FILES)
        if r_form.is_valid() and a_form.is_valid():
            email = r_form.cleaned_data['email'].lower()
            password = r_form.cleaned_data['password1']
            first_name = r_form.cleaned_data.get('first_name', '')
            last_name = r_form.cleaned_data.get('last_name', '')

            # Хэрэглэгч үүсгэх
            user = User.objects.create_user(username=email, email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)
            account = a_form.save(commit=False)
            account.user = user
            account.save()

            messages.success(request, "Бүртгэл амжилттай. Нэвтрэх хэсгээр орно уу.")
            return redirect('signin')
        else:
            messages.error(request, "Бүртгэлийн явцад алдаа гарлаа. Формын алдааг шалгана уу.")
    else:
        r_form = RegisterForm()
        a_form = AccountForm()

    return render(request, "register.html", {"u_form": r_form, "a_form": a_form})


def user_login(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip().lower()
        password = request.POST.get("password", "")

        # authenticate by username (we saved username = email)
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # try phone-number -> find user with account.phone_number == identifier
            try:
                acc = Account.objects.get(phone_number=identifier)
                user = authenticate(request, username=acc.user.username, password=password)
            except Account.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name or user.username}!")
            return redirect('/')  # index
        else:
            messages.error(request, "Нэвтрэх: буруу цахим шуудан/утас эсвэл нууц үг.")
            return redirect(':signin')

    return render(request, "signin.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Та гарлаа.")
    return redirect('signin')


@login_required
def profile_view(request):
    account, created = Account.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'account': account})


@login_required
def profile_edit(request):
    user = request.user
    account, _ = Account.objects.get_or_create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        a_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, "Амжилттай шинэчлэгдлээ")
            return redirect('profile')
        else:
            messages.error(request, "Алдаа гарлаа. Алдаануудыг шалгана уу.")
    else:
        u_form = UserUpdateForm(instance=user)
        a_form = AccountUpdateForm(instance=account)

    context = {
        'u_form': u_form,
        'a_form': a_form,
        'account': account,
    }
    return render(request, 'accounts/profile_edit.html', context)
