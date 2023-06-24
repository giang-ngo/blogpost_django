from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserForm, MyUserCreateForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('posts')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not existed.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts')
        else:
            messages.error(request, 'Email or password does not existed.')

    context = {}
    return render(request, 'users/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('posts')


def registerPage(request):
    form = MyUserCreateForm()
    if request.method == 'POST':
        form = MyUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration.')
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all().exclude(approved=False)
    messages_post = user.message_set.all().order_by('-created')[0:5]
    context = {'user': user, 'posts': posts,
               'messages_post': messages_post}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form': form}
    return render(request, 'users/update_user.html', context)


@login_required(login_url='login')
def passwordChange(request):
    user = request.user
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            return redirect('posts')
        else:
            messages.error(
                request, 'An error occurred during password change.')
    context = {'form': form}
    return render(request, 'users/password_change.html', context)


def passwordResetRequest(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Blogpost password reset'
                    email_template_name = 'users/password_message.txt'
                    parameters = {
                        'username': user.username,
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Blogpost',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [
                                  user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
            else:
                messages.error(request, 'Your email does not exist')
    context = {'form': form}
    return render(request, 'users/password_reset.html', context)
