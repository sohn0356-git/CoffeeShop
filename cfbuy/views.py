import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect, reverse

from cfbuy.models import *
from cfproduct.models import CftoOption
from cfuser.models import Cfuser

# Create your views here.
def buy_complete(request):
    cfbuy = Cfbuy()
    cfbuy.buyer = Cfuser.objects.get(email=request.session['user'])
    cfbuy.recipient = request.POST.get('recipient')
    cfbuy.postcode = request.POST.get('postcode')
    cfbuy.address = request.POST.get('address')
    cfbuy.detailAddress = request.POST.get('detailAddress')
    cfbuy.extraAddress = request.POST.get('extraAddress')
    cfbuy.phone1 = request.POST.get('phone1')
    cfbuy.phone2 = request.POST.get('phone2')
    cfbuy.phone3 = request.POST.get('phone3')
    cfbuy.phone = request.POST.get('phone1') + request.POST.get('phone2') + request.POST.get('phone3')
    cfbuy.email_name = request.POST.get('email')
    cfbuy.email_domain = request.POST.get('domain')
    cfbuy.email = request.POST.get('email')+ '@' + request.POST.get('domain')
    cfbuy.buy_method = request.POST.get('buy_method')
    cfbuy.delivery_msg = request.POST.get('deliverymsg')
    print(request.POST)
    cfbuy.save()

    options = eval(request.POST.get('options'))
    
    for option in options:
        buysum = 0
        buydetail = Buydetail()
        buydetail.buy_info = cfbuy
        buydetail.quantity = option[0]['quantity']
        buydetail.save()
        print(option[0])
        for ol in option[0]['option_list']:
            cfselect = Cfselect()
            cfselect.cfoption = CftoOption.objects.get(id=ol)
            cfselect.cf_code = cfselect.cfoption.coffee_id.cfcode
            cfselect.buy = buydetail
            buysum += buydetail.quantity * cfselect.cfoption.amount
            cfselect.save()
        
        buydetail.amount = buysum
        buydetail.save()

    return redirect(reverse('cfbuy:order_list'))

def order_list(request):
    res_data={}
    user = Cfuser.objects.get(email=request.session['user'])
    orders = Cfbuy.objects.filter(buyer=user).order_by('-buy_date')
    res_data['order_list'] = []
    for order in orders:
        buydetails = Buydetail.objects.filter(buy_info=order)
        cfselects = []
        for buydetail in buydetails:
            cfselect = Cfselect.objects.filter(buy=buydetail)
            cfselects.append(cfselect)
        res_data['order_list'].append([order, cfselects, buydetails])
    return render(request, 'cfbuy/cfbuy_list.html', res_data)

def show_graph(request):
    buydetails = set()
    sold_cf = {}
    cf_code = Coffeecode.objects.get(cfcode='SINGLE ORIGINS')
    cf_names = Cfproduct.objects.filter(cfcode=cf_code)
    for cf_name in cf_names:
        sold_cf[cf_name.name]=0
    cfselects = Cfselect.objects.filter(cf_code=cf_code)
    for cfselect in cfselects:
        buydetails.add((cfselect.cfoption.coffee_id.name,cfselect.buy))
    for buydetail in buydetails:
        if buydetail[1]:
            sold_cf[buydetail[0]] += buydetail[1].quantity
    res_data = {'sold_cf':json.dumps(sold_cf)}
    return render(request, 'graph.html', res_data)