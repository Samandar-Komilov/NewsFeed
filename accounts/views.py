from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import LoginForm, UserRegistrationForm

# Sample user login function
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  # validated_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])  # data orqali user auth qilindi
            print(">>> USER >>>",user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("✅ Muvaffaqiyatli login amalga oshirildi!")
                else:
                    return HttpResponse("⏳ Sizning profilingiz faol holatda emas!")
                
            else:
                return HttpResponse("🚫 Bunday user topilmadi! Login yoki parol kiritishda xatolik mavjud!")
    else:
        form = LoginForm()     # GET method bolsa muammo yoq, directly form yasaymiz, aks holda esa auth qilamiz.
    context = {
        'form':form,
    }
    return render(request, 'account/login.html', context)

@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user':user,
        'profile':profile,
    }
    return render(request, 'pages/user_profile.html', context)


# User registration View
def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Profiles uchun model ochish

            context = {
                'new_user':new_user,
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form':user_form,
        }
    return render(request, 'account/register.html', context)


# Class View | We can use one of them!
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'

class SignUpView(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        context = {
            'user_form':user_form,
        }
        return render(request, 'account/register.html', context)

    def post(self, request):
        if request.method == "POST":
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                # New user create qilinishi bilan Profile da ham create qilinadi
                Profile.objects.create(user=new_user)
                context = {
                    'new_user':new_user,
                }
                return render(request, 'account/register_done.html', context)
            
# EDIT PROFILE
@login_required
def edit_user(request):
    if request.method == 'POST':
        # User va Profile formlarni alohida ochiladi
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request, 'account/profile_edit.html', context)

# EDIT Class based
class EditUserView(LoginRequiredMixin,View):
    # LoginRequiredMixin - if user did not log in, it redirects him to Login page
    def get(self,request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form':user_form,
            'profile_form':profile_form,
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self,request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')