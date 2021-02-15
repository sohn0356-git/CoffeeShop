import json, requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, redirect, reverse
from django.db.models import Q

from cfbuy.models import *
from cfproduct.models import CftoOption
from cfuser.models import Cfuser

buy_id_list = []
basket_id_list = []

# Create your views here.
def buy_complete(request):
    baskets = request.POST.get('baskets')
    if baskets:
        baskets = eval(baskets)
        for b in baskets:
            basket_id_list.append(b)


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
    cfbuy.save()
    buy_id_list.append(cfbuy.id)

    options = eval(request.POST.get('options'))
    
    for option in options:
        buysum = 0
        price = 0
        buydetail = Buydetail()
        buydetail.buy_info = cfbuy
        buydetail.quantity = option[0]['quantity']
        buydetail.save()
        for ol in option[0]['option_list']:
            cfselect = Cfselect()            
            cfselect.cfoption = CftoOption.objects.get(id=ol)
            price = cfselect.cfoption.coffee_id.price
            cfselect.cf_code = cfselect.cfoption.coffee_id.cfcode
            cfselect.buy = buydetail
            
            buysum += buydetail.quantity * cfselect.cfoption.amount
            cfselect.save()
        
        buydetail.amount = buysum + buydetail.quantity * price
        buydetail.save()
    
    return redirect(reverse('cfbuy:kakao_pay'))
    
    # return redirect(reverse('cfbuy:order_list'))

def order_list(request):
    res_data={}
    user = Cfuser.objects.get(email=request.session['user'])
    orders = None
    print(request.POST)
    if request.method == "POST" and request.POST.get('search')!='reset':
        startdate = request.POST.get('start_date')
        enddate = request.POST.get('end_date')
        if startdate and enddate:
            orders = Cfbuy.objects.filter(buyer=user).filter(buy_date__range=[startdate, enddate]).order_by('-buy_date')
    else :
        enddate = datetime.today()
        startdate = enddate - relativedelta(months=3)
        orders = Cfbuy.objects.filter(buyer=user).filter(buy_date__range=[startdate, enddate]).order_by('-buy_date')

    res_data['order_list'] = []
    if orders:
        for order in orders:
            buydetails = Buydetail.objects.filter(buy_info=order)
            cfselects = []
            for buydetail in buydetails:
                cfselect = Cfselect.objects.filter(buy=buydetail)
                cfselects.append(cfselect)
            res_data['order_list'].append([order, cfselects, buydetails])
    return render(request, 'cfbuy/cfbuy_list.html', res_data)

def show_graph(request):
    year = datetime.today().year
    month = datetime.today().month
    res_data = {}
    sold_cf = {}
    names = {}
    cf_codes = Coffeecode.objects.all()
    for cf_code in cf_codes:
        cf_names = Cfproduct.objects.filter(cfcode=cf_code)
        

        for cf_name in cf_names:
            if names.get(cf_code.cfcode):
                names[cf_code.cfcode].append(cf_name.name)
            else:
                names[cf_code.cfcode] = [cf_name.name]
        
        sold_cf[cf_code.cfcode] = {}
        for m in range(0,6):
            nm = month - m
            ny = year
            if nm < 1:
                nm = nm + 12
                ny -= 1
            buydetails = set()
            year_month = str(ny)+'-'+str(nm)
            sold_cf[cf_code.cfcode][year_month] = {}
            
            for cf_name in cf_names:
                sold_cf[cf_code.cfcode][year_month][cf_name.name]=0
            cfselects = Cfselect.objects.filter(cf_code=cf_code).filter(~Q(buy__isnull=True)).filter(buy_date__year=ny).filter(buy_date__month=nm)
            for cfselect in cfselects:
                buydetails.add((cfselect.cfoption.coffee_id.name,cfselect.buy))
            for buydetail in buydetails:
                sold_cf[cf_code.cfcode][year_month][buydetail[0]] += buydetail[1].quantity

    res_data['sold_cf']=json.dumps(sold_cf)
    res_data['names']=json.dumps(names)
    return render(request, 'graph.html', res_data)

def kakaopay(request):
    buy_info = Cfbuy.objects.get(id=buy_id_list[0])
    buy_details = Buydetail.objects.filter(buy_info=buy_info)
    options = []
    buysum = 0
    
    name = ''
    names = set()
    total_quantity = 0
    quantity = []
    for buy_detail in buy_details:
        quantity.append(buy_detail.quantity)
        total_quantity += quantity[-1]
        options.append(Cfselect.objects.filter(buy=buy_detail))
    
    email = request.session['user']
    
    for idx, option in enumerate(options):
        price = 0
        names.add(option[0].cfoption.coffee_id.name)
        for ol in option:
            price = ol.cfoption.coffee_id.price  
            buysum += quantity[idx] * ol.cfoption.amount
        buysum = buysum + quantity[idx] * price
    
    for n in names:
        name += '[ '+ n + ' ]' + ' / '
    name = name[:-2]
    
    _admin_key = '6f1fe2f59f109a08501d463674bb96d7'
    _url = f'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}',
    }
    _data = {
        'cid': 'TC0ONETIME',
        'partner_order_id': str(buy_id_list[0]),
        'partner_user_id': email,
        'item_name': name,
        'quantity': total_quantity,
        'total_amount': buysum,
        'tax_free_amount':'0',
        # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
        # * 등록 : http://IP:8000 
        # 'approval_url': reverse('cfbuy:approve'),
        'approval_url': 'http://127.0.0.1:8000/buy/approve',
        'fail_url':'http://127.0.0.1:8000/payFail',
        'cancel_url':'http://127.0.0.1:8000/payCancel'
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    request.session['tid'] = _result['tid']
    return redirect(_result['next_redirect_pc_url'])
    # request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
    # next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
    # return redirect(next_url)

    return render(request, 'cfbuy/kakao_pay.html')

def approval(request):
    email = request.session['user']
    _admin_key = '6f1fe2f59f109a08501d463674bb96d7'
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id': str(buy_id_list[0]),
        'partner_user_id':  email,
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    context = {
        'res': _result,
    }
    if _result.get('msg'):
        cfbuy = Cfbuy.objects.get(id=buy_id_list[0])
        cfbuy.delete()
        buy_id_list.clear()
        basket_id_list.clear()
        return redirect('/')
    else:
        for b in basket_id_list:
            basketdetail = Basketdetail.objects.get(id=b)
            basketdetail.delete()
        basket_id_list.clear()
        buy_id_list.clear()
        return render(request, 'cfbuy/approval.html', context)