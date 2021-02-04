from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F

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

def cfselect(request,id):
    cfproduct = Cfproduct.objects.get(id=id)
    res_data = {'coffee' : cfproduct}
    cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    res_data['option_list'] = []
    option_set = set()
    for cftooption in cftooptions:
        option_id = cftooption.option_id.id
        cfoption = Cfoption.objects.get(id=option_id)
        res_data['option_list'].append(cfoption)
        option_set.add(cfoption.code_option)
    res_data['option_set'] = option_set
    return render(request, 'cfproduct/product_detail.html',res_data)


def buydetail(request):
    id = request.POST.get('id')
    cfproduct = Cfproduct.objects.get(id=id)
    res_data = {'select_list' : [], 'coffee' : cfproduct, 'quantity' : 1}
    # quantity = request.POST.get('quantity')
    cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    
    for cftooption in cftooptions:
        option_id = cftooption.option_id.id
        cfoption = Cfoption.objects.get(id=option_id)
        if request.POST.get(cfoption.code_option.title)==str(cfoption.id):
            cfselect = Cfselect()
            cfselect.cfoption = cftooption
            cfselect.save()
            res_data['select_list'].append(cfselect)
   
    return render(request, 'cfbuy/buydetail.html',res_data)

 
