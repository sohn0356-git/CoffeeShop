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
    cfbuy.roadAddress = request.POST.get('roadAddress')
    cfbuy.jubunAddress = request.POST.get('jubunAddress')
    cfbuy.detailAddress = request.POST.get('detailAddress')
    cfbuy.phone = request.POST.get('phone1') + request.POST.get('phone2') + request.POST.get('phone3')
    cfbuy.email = request.POST.get('email')+ '@' + request.POST.get('domain')
    cfbuy.buy_method = request.POST.get('buy_method')
    cfbuy.save()

    options = eval(request.POST.get('options'))
    
    for option in options:
        buysum = 0
        buydetail = Buydetail()
        buydetail.buy_info = cfbuy
        buydetail.save()
        for ol in option[0]['option_list']:
            cfselect = Cfselect()
            cfselect.cfoption = CftoOption.objects.get(id=ol)
            cfselect.quantity = option[0]['quantity']
            cfselect.buy = buydetail
            buysum += cfselect.quantity * cfselect.cfoption.amount
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
        res_data['order_list'].append([order,cfselects, buydetails])
    return render(request, 'cfbuy/cfbuy_list.html', res_data)