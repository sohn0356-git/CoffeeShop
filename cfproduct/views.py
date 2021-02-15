from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
import json

from cfproduct.models import *
from cfbuy.models import Cfselect, Basketdetail, Cfbuy
# Create your views here.

def index(request):
    return render(request, 'cfproduct/index.html', { 'email': request.session.get('user') })

def coffee(request, pk):
    res_data = {'pk' : pk}
    cfcode = Coffeecode.objects.get(id=pk)
    try:
        coffee_list = Cfproduct.objects.filter(cfcode=cfcode).order_by('id')
        res_data['cfcode'] = cfcode
        res_data['coffee_list'] = coffee_list
        paginator = Paginator(coffee_list, 6) # Show 6 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        res_data['page_obj'] = page_obj
        
    except Cfproduct.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'cfproduct/product.html', res_data)

def cfcreate(request):
    cfproduct = Cfproduct()
    cfproduct.name = request.POST['name']
    cfproduct.price = int(request.POST['price'])
    cfproduct.image = request.FILES['images']
    cfproduct.cfcode = Coffeecode.objects.get(id=1)
    cfproduct.save()
    return redirect(reverse('cfproduct:coffee', kwargs={'pk': 1}))

def product_detail(request,id):
    cfproduct = Cfproduct.objects.get(id=id)
    res_data = {'coffee' : cfproduct}
    res_data['id'] = id
    cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    res_data['cftooptions'] = cftooptions
    comments = Cfcomment.objects.filter(coffee=cfproduct)
    comment = []
    for idx, c in enumerate(comments):
        comment.append([(idx+1)%2, c])
    res_data['comments'] = comment
    option_set = set()
    price_info = {}
    for cftooption in cftooptions:
        code_option = cftooption.option_id.code_option
        price_info[cftooption.id]=cftooption.amount
        option_set.add(code_option)
    price_info['len'] = len(option_set)
    price_info['base'] = cfproduct.price
    res_data['priceJson'] = json.dumps(price_info)
    res_data['option_set'] = option_set
    return render(request, 'cfproduct/product_detail.html',res_data)


def buy_detail(request):
    id = request.POST.get('id')
    res_data = {}
    if request.method == 'POST':
        cart_or_buy = request.POST.get('buy')
        cfproduct = Cfproduct.objects.get(id=id)
        res_data['coffee'] = cfproduct    
        options = (eval(str(request.POST.get('option'))))
        cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)

        options_info_id = []
        options_info = []
        quan_dict = {}
        total_sum = 0
        if options:
            if cart_or_buy == 'buy':
                user = Cfuser.objects.get(email=request.session['user'])
                recent_buy = Cfbuy.objects.filter(buyer=user).order_by('-buy_date')
                if recent_buy:
                    recent_buy = recent_buy[0]
                res_data['recent_buy'] = recent_buy

                for k, v in options.items():
                    if len(v)>2:
                        options_info.append([])
                        options_info_id.append([])
                        option_list = []
                        option_list_id = []
                        for i in v[:-2]:
                            target = CftoOption.objects.get(id=i)
                            option_list.append(target)
                            option_list_id.append(i)
                        total_sum += v[-1]*v[-2]
                        options_info[-1].append({'option_list':option_list,'quantity':v[-2],'price':v[-1], 'sum':v[-2]*v[-1]})
                        options_info_id[-1].append({'option_list':option_list_id, 'quantity':v[-2]})
                if len(options_info):
                    res_data['total_sum'] = total_sum
                    res_data['cftooptions'] = cftooptions
                    res_data['options_info'] = options_info
                    res_data['options_info_id'] = options_info_id
                    res_data['quantitys'] = quan_dict
                    return render(request, 'cfbuy/buy_page.html', res_data)
            else: 
                user = Cfuser.objects.get(email=request.session['user'])
                for k, v in options.items():
                    basketdetail = Basketdetail()
                    basketdetail.buyer = user
                    basketdetail.save()
                    basketsum = 0
                    quantity = 0
                    if len(v)>2:
                        for i in v[:-2]:
                            target = CftoOption.objects.get(id=i)
                            cfselect = Cfselect()
                            cfselect.cfoption = CftoOption.objects.get(id=i)
                            cfselect.cf_code = cfselect.cfoption.coffee_id.cfcode
                            cfselect.basket = basketdetail
                            cfselect.save()
                    
                    basketdetail.quantity = v[-2]
                    basketdetail.amount = v[-1]
                    basketdetail.total = basketdetail.quantity * basketdetail.amount
                    basketdetail.save()
                
                return redirect(reverse('cfuser:cart'))
   
    return redirect(reverse('cfproduct:coffee_detail', kwargs={'id': id}))

 
def product_comment(request, id):
    errors = []
    if request.method == "POST":
        user = Cfuser.objects.get(email=request.session['user'])
        coffee = Cfproduct.objects.get(id=id)
        contents = request.POST.get('contents')

        if not contents:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Cfcomment.objects.create(coffee=coffee, user=user, contents=contents)
            return redirect(reverse('cfproduct:coffee_detail', kwargs={'id' : id}))

    return redirect(reverse('cfproduct:coffee_detail', kwargs={'id' : id}))