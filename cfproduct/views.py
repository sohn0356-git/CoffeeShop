from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cfproduct/product.html', { 'email': request.session.get('user') })
