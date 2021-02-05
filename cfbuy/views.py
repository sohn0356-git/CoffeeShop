from django.shortcuts import render

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
        buydetail = Buydetail()
        buydetail.buy_info = cfbuy
        buydetail.save()

        for ol in option[0]['option_list']:
            cfselect = Cfselect()
            cfselect.cfoption = CftoOption.objects.get(id=ol)
            cfselect.quantity = option[0]['quantity']
            cfselect.buy = buydetail
            cfselect.save()       

    return render(request, 'cfbuy/test.html')