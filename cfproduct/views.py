from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator

from cfproduct.models import *
# Create your views here.

def index(request):
    return render(request, 'cfproduct/index.html', { 'email': request.session.get('user') })

def coffee(request, pk):
    res_data = {'pk' : pk}
    cfcode = Coffeecode.objects.get(id=pk)
    try:
        coffee_list = Cfproduct.objects.filter(cfcode=cfcode)
        res_data['cfcode'] = cfcode
        res_data['coffee_list'] = coffee_list
        paginator = Paginator(coffee_list, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        res_data['page_obj'] = page_obj
        
    except Cfboard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'cfproduct/coffee.html', res_data)

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
    cfoptions = CftoOption.objects.filter(coffee_id=cfproduct)
    res_data['option_list'] = []
    for option in cfoptions:
        optionid = option.option_id
        optiondetail = Optiondetail.objects.filter(option_id=optionid)
        res_data['option_list'].append({optionid:optiondetail})
    return render(request, 'cfproduct/cfselect.html',res_data)


def buydetail(request):
    id = request.POST.get('id')
    cfproduct = Cfproduct.objects.get(id=id)
    res_data= {'option_list' : []}
    cftooptions = CftoOption.objects.filter(coffee_id=cfproduct)
    # quantity = request.POST.get('quantity')
    for cftooption in cftooptions:
        detail_id = (request.POST.get(cftooption.option_id.title))
        res_data['option_list'].append(Optiondetail.objects.get(id=detail_id))
    for r in res_data['option_list']:
        print(r.option_id,' ',r.option,' ',r.amount)
        # print(request.POST.get(option_id.title))
    # res_data = {'quantity':quantity}
    # buyer = Cfuser.objects.get(email=request.session['user'])
    return redirect(reverse('cfproduct:cfselect', kwargs={'id': id}))

def cfbuy(request):
    pass

    
        
