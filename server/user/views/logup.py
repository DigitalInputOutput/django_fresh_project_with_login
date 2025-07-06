from django.views.generic import View
from user.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from json import loads
from simple_app.utils import is_ajax

class LogupView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        html_template = 'base.html' if is_ajax(request) else 'index.html'

        context = {
            'base': html_template,
            'form': UserCreationForm(),
            'h1': _('Registration')
        }

        return render(request, 'user/logup.html', context)

    def post(self,request,*args,**kwargs):
        if is_ajax(request):
            try:
                data = loads(request.body.decode('utf-8'))
            except Exception as e:
                return JsonResponse({"error":"Error parsing json"})
        else:
            data = request.POST

        form = UserCreationForm(data)

        if form.is_valid():
            user = form.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)

            if is_ajax(request):
                return JsonResponse({
                    'href':request.META.get('HTTP_REFERER','/')
                })
            else:
                return redirect(request.META['HTTP_REFERER'])
        else:
            html_template = 'base.html' if is_ajax(request) else 'index.html'

            context = {
                'base': html_template,
                'form': form,
                'error': _('Form error.')
            }

        return render(request, 'user/logup.html', context)