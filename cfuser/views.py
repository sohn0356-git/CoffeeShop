import os, json

from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from cfuser.forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from cfuser.models import Cfuser
from cfbuy.models import Basketdetail, Cfselect
from django.conf import settings
from datetime import datetime

from cfproduct.models import CftoOption
from cfbuy.models import Basketdetail, Cfselect, Cfbuy
# Create your views here.

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

class RegisterView(FormView):
    template_name = 'cfuser/register.html'
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
    template_name = 'cfuser/login.html'
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


def cart(request):
    user = Cfuser.objects.get(email=request.session['user'])
    baskets = Basketdetail.objects.filter(buyer=user).order_by('-id')
    res_data = {'baskets':[]}
    if request.method=="POST":
        btn = request.POST.get('btn')
        checkboxs = request.POST.getlist('checkbox')
        if btn=='delete':            
            for checkbox in checkboxs:
                basketdetail = Basketdetail.objects.filter(id=checkbox)
                if basketdetail:
                    basketdetail.delete()
        else:
            total_sum = 0
            options_info_id = []
            options_info = []
            quan_dict = {}
            basketdetails = []
            user = Cfuser.objects.get(email=request.session['user'])
            recent_buy = Cfbuy.objects.filter(buyer=user).order_by('-buy_date')
            if recent_buy:
                recent_buy = recent_buy[0]
            res_data['recent_buy'] = recent_buy


            if btn=='selectbuy':
                for checkbox in checkboxs:
                    basketdetail = Basketdetail.objects.get(id=checkbox)
                    if basketdetail:
                        basketdetails.append(basketdetail)
            elif btn=='allbuy' :
                basketdetails = Basketdetail.objects.filter(buyer=user)
                checkboxs = set()
                for b in basketdetails:
                    checkboxs.add(b.id)

            res_data['baskets'] = checkboxs
            
            
            for basketdetail in basketdetails:
                print(basketdetail)
                options_info.append([])
                options_info_id.append([])
                option_list = []
                option_list_id = []
                quantity = basketdetail.quantity
                price = 0
                cfselects = Cfselect.objects.filter(basket=basketdetail)
                for cfselect in cfselects:
                    option_list.append(cfselect.cfoption)
                    price += cfselect.cfoption.amount
                    option_list_id.append(cfselect.cfoption.id)
                price += option_list[0].coffee_id.price
                total_sum += price*quantity
                options_info[-1].append({'coffee' : option_list[0].coffee_id,'option_list':option_list,'quantity':quantity,'price':price, 'sum':quantity*price})
                options_info_id[-1].append({'option_list':option_list_id, 'quantity':quantity})

            if len(options_info):
                res_data['total_sum'] = total_sum
                res_data['options_info'] = options_info
                res_data['options_info_id'] = options_info_id
                res_data['quantitys'] = quan_dict
                return render(request, 'cfbuy/buy_page.html', res_data)

    if baskets:
        for basket in baskets:
            cfselects = Cfselect.objects.filter(basket=basket)
            res_data['baskets'].append([basket,cfselects])
    return render(request, 'cfbuy/cart.html', res_data)

def profile(request):
    res_data = {}
    msg = {}
    user = Cfuser.objects.get(email=request.session['user'])
    res_data['user'] = user
    if request.method=="POST":
        print(request.POST)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        image = request.FILES.get('image')

        if password != repassword:
            msg['error'] = "패스워드가 일치하지 않습니다."
            res_data['msg'] = json.dumps(msg)

        if not msg.get('error'):
            user.name = name
            if password:
                user.password = make_password(password)
            user.phone = phone
            user.level = 'user'
            if image:
                user.image = image
            user.save()
    return render(request,'cfuser/profile.html',res_data)
