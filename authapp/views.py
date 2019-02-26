from django.shortcuts import render

from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import LoginForm, RegisterForm, EditForm
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import SystemUser
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'Sign in'
    login_form = LoginForm(data=request.POST)
    error_message = ''
    info_message = ''

    try:
        info_message = request.session['info_message']
        error_message = request.session['error_message']
    except Exception:
        print("wrong with session")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:main'))
        else:
            error_message = "User does not exist (might be is not active) or password is wrong!"
    else:
        try:
            if request.session['send_is_ok']:
                info_message = "Activation key has been sent to your email. Please check and activate the account!"
            else:
                request.session['send_is_not_ok']
                error_message = "Error during sending email with activation code!"
        except Exception:
            pass

    print(info_message)
    content = {'title': title,
               'login_form': login_form,
               'error_message': error_message,
               'info_message': info_message}

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))


def register(request):
    title = 'Register'
    error_message = ''
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('Сообщение подтверждения отправлено')
                request.session['send_is_ok'] = True
            else:
                print('Ошибка отправки сообщения')
                request.session['send_is_not_ok'] = True
                del request.session['send_is_ok']
        else:
            error_message = "Passwords are not identical"
            content = {'title': title, 'register_form': register_form, 'error_message': error_message}
            return render(request, 'authapp/register.html', content)
        return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = RegisterForm()
        content = {'title': title, 'register_form': register_form}
        return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = EditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = EditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = SystemUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            request.session['info_message'] = 'Activation has done successfully. Please sign in!'
            request.session['error_message'] = f''
        else:
            request.session['info_message'] = ''
            request.session['error_message'] = f'Error activation user: {user.username}'
            print(f'error activation user: {user.username}')

        try:
            del request.session['send_is_ok']
        except Exception:
            pass
        return HttpResponseRedirect(reverse('authapp:login'))

    except Exception as e:
        print(f'error activation user : {e.args}')
        request.session['error_message'] = f'Error during activation user!'
        # return render(request, 'authapp/register.html')
        return HttpResponseRedirect(reverse('authapp:login'))


def reset(request):
    pass

