from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm, AccountForm, UserUpdateForm, AccountUpdateForm
from .models import Account


def user_register(request):
    if request.method == "POST":
        r_form = RegisterForm(request.POST)
        a_form = AccountForm(request.POST, request.FILES)

        if r_form.is_valid() and a_form.is_valid():
            email = r_form.cleaned_data['email'].lower()
            password = r_form.cleaned_data['password1']
            first_name = r_form.cleaned_data.get('first_name', '')
            last_name = r_form.cleaned_data.get('last_name', '')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            account = a_form.save(commit=False)
            account.user = user
            account.save()

            messages.success(request, "Бүртгэл амжилттай. Нэвтрэх хэсгээр орно уу.")
            return redirect('signin')

        messages.error(request, "Форм алдаатай байна. Шалгана уу.")
    else:
        r_form = RegisterForm()
        a_form = AccountForm()

    return render(request, "register.html", {"u_form": r_form, "a_form": a_form})


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower()
        password = request.POST.get("password", "")

        # email == username
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Сайн уу, {user.first_name or user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Нэвтрэх мэдээлэл буруу байна.")
            return redirect('signin')

    return render(request, "signin.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Та амжилттай гарлаа.")
    return redirect('signin')


@login_required
def profile_view(request):
    account, _ = Account.objects.get_or_create(user=request.user)
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

        messages.error(request, "Форм алдаатай байна.")
    else:
        u_form = UserUpdateForm(instance=user)
        a_form = AccountUpdateForm(instance=account)

    return render(request, 'accounts/profile_edit.html', {
        'u_form': u_form,
        'a_form': a_form,
        'account': account,
    })
