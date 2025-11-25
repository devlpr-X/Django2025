# from django.shortcuts import render, redirect
# from django.contrib import messages, auth
# from .forms import RegisterForm, AccountForm
# from django.contrib.auth import authenticate, login, logout

# def user_register(request):
#     if request.method == "POST":
#         u_form = RegisterForm(request.POST)
#         a_form = AccountForm(request.POST, request.FILES)
#         if u_form.is_valid() and a_form.is_valid():
#             user = u_form.save()
#             account = a_form.save(commit=False)
#             account.user = user
#             account.save()
#             messages.success(request, "Бүртгэл амжилттай. Нэвтрэх хэсгээр орно уу.")
#             return redirect('signin')
#         else:
#             messages.error(request, "Бүртгэлийн явцад алдаа гарлаа. Доорх талбаруудыг шалгана уу.")
#     else:
#         u_form = RegisterForm()
#         a_form = AccountForm()

#     return render(request, "register.html", {"u_form": u_form, "a_form": a_form})


# def user_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email", "").strip().lower()
#         password = request.POST.get("password", "")

#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome {user.first_name or user.username}!")
#             return redirect('/')  
#         else:
#             messages.error(request, "Нэвтрэх: буруу цахим шуудан эсвэл нууц үг.")
#             return redirect('signin')

#     return render(request, "signin.html")


# def user_logout(request):
#     logout(request)
#     messages.info(request, "Та гарлаа.")
#     return redirect('signin')
