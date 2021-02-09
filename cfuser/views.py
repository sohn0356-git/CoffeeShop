from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from cfuser.forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from cfuser.models import Cfuser
from cfbuy.models import Basketdetail, Cfselect
# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        cfuser = Cfuser(
            email=form.data.get('email'),
            name=form.data.get('name'),
            password=make_password(form.data.get('password')),
            phone=form.data.get('phone'),
            level='user'
        )
        cfuser.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        cfuser = Cfuser.objects.get(email=form.data.get('email'))
        self.request.session['mode'] = cfuser.level

        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')


class UserLV(ListView):
    model = Cfuser

def cart(request):
    user = Cfuser.objects.get(email=request.session['user'])
    baskets = Basketdetail.objects.filter(buyer=user)
    res_data = {'baskets':[]}
    for basket in baskets:
        cfselects = Cfselect.objects.filter(basket=basket)
        res_data['baskets'].append([basket,cfselects])
    return render(request, 'cfbuy/cart.html', res_data)