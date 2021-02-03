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
    return render(request, 'cfproduct/buy.html',res_data)

def buydetail(request):
    quantity = request.POST.get('quantity')
    res_data = {'quantity':quantity}
    buyer = Cfuser.objects.get(email=request.session['user'])
    recent_buy_info = BuyInfo.objects.filter(buyer=buyer).order_by('-buy_date')

def cfbuy(request):
    pass

    
        
