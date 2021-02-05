from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
import json

from cfproduct.models import *
from cfbuy.models import Cfselect
# Create your views here.

def index(request):
    return render(request, 'cfproduct/index.html', { 'email': request.session.get('user') })

def coffee(request, pk):
    res_data = {'pk' : pk}
    cfcode = Coffeecode.objects.get(id=pk)
    try:
        coffee_list = Cfproduct.objects.filter(cfcode=cfcode).order_by('id')
        coffee_list = coffee_list.annotate(row_number=Window(
            expression=RowNumber(),
            partition_by=[F('cfcode')])
        )
        for c in coffee_list:
            c.row_number = c.row_number%3
        res_data['cfcode'] = cfcode
        res_data['coffee_list'] = coffee_list
        paginator = Paginator(coffee_list, 6) # Show 25 contacts per page.
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
    cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    res_data['cftooptions'] = cftooptions
    option_set = set()
    for cftooption in cftooptions:
        code_option = cftooption.option_id.code_option
        option_set.add(code_option)
    res_data['option_set'] = option_set
    return render(request, 'cfproduct/product_detail.html',res_data)


def buy_detail(request):
    id = request.POST.get('id')
    res_data = {}
    if request.method == 'POST':        
        cfproduct = Cfproduct.objects.get(id=id)
        options = (eval(str(request.POST.get('test'))))
        cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    
        options_info = []
        quan_dict = {}
        for k, v in options.items():
            if len(v)>1:
                options_info.append([])
                option_list = []
                for i in v[:-1]:
                    option_list.append(CftoOption.objects.get(id=i))
                options_info[-1].append({'option_list':option_list,'quantity':v[-1]})

        res_data['cftooptions'] = cftooptions
        res_data['coffee'] = cfproduct
        res_data['options_info'] = options_info
        res_data['quantitys'] = quan_dict    
    # quantity = request.POST.get('quantity')
    # res_data = {'select_list' : [], 'coffee' : cfproduct, 'quantity' : quantity}    
    # cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    
    # for cftooption in cftooptions:
    #     option_id = cftooption.option_id.id
    #     cfoption = Cfoption.objects.get(id=option_id)
    #     if request.POST.get(cfoption.code_option.title)==str(cfoption.id):
    #         cfselect = Cfselect()
    #         cfselect.cfoption = cftooption
    #         cfselect.save()
    #         res_data['select_list'].append(cfselect)
   
    return render(request, 'cfbuy/buy_page.html', res_data)
    # return render(request, 'cfbuy/buydetail.html',res_data)

 
