from django.views.generic import View
from user.forms import LogInForm
from django.forms.utils import ErrorList
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from user.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from json import loads
from simple_app.utils import is_ajax

__all__ = ['LoginView','authenticate']

class LoginView(View):
    template = ''

    def get(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            html_template = 'base.html' if is_ajax(request) else 'index.html'

            context = {
                'base': html_template,
                'next': request.GET.get('next'),
                'form': LogInForm()
            }

            return render(request, 'user/login.html',context)

        # user is already logged in
        elif is_ajax(request):
            return JsonResponse({'result':True})
        elif request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('/')

    def post(self,request,*args,**kwargs):
        if is_ajax(request):
            try:
                data = loads(request.body)
            except:
                return JsonResponse({"error":"Error loading json"})
        else:
            data = request.POST

        if request.user.is_anonymous:
            html_template = 'base.html' if is_ajax(request) else 'index.html'

            form = LogInForm(data)

            if form.is_valid():
                user = authenticate(value=form.cleaned_data['login'], password=form.cleaned_data['password'])

                if user is not None and is_ajax(request):
                    login(request, user)
                    return JsonResponse({'result':True})

                elif user is not None:
                    login(request,user)
                    next = data.get('next')

                    if next:
                        return redirect(next)
                    else:
                        return redirect('/')
                else:
                    errors = form._errors.setdefault("__all__", ErrorList())
                    errors.append(_("Password does not match"))
            else:
                errors = form._errors.setdefault("__all__", ErrorList())
                errors.append(_("Password does not match"))

            context = {
                'base': html_template,
                'form': form,
            }

            return render(request, 'user/login.html',context)

        # user is already logged in
        elif is_ajax(request):
            return JsonResponse({'result':True})

        elif request.GET.get('next'):
            return redirect(request.GET.get('next'))

        else:
            return redirect('/')

def find(key,value):
    params = {key:value}

    try:
        return [User.objects.get(**params)]
    except User.MultipleObjectsReturned:
        return User.objects.filter(**params)
    except User.DoesNotExist:
        return []

def authenticate(value=None, password=None):
    for key in ['login']:
        users = find(key,value)
        if users:
            break

    for user in users:
        if check_password(password, user.password):
            user.last_login = timezone.now()
            return user
    return None