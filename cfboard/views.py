from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from cfboard.models import *

# Create your views here.
def index(request):
    return render(request, 'board.html')

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Cfboard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'board_detail.html', {'board': board})
    

def boards(request, b):
    res_data = {}
    try:
        boardname = b
        boards = Cfboard.objects.filter(boardname=boardname)
        if boards:
            res_data['boardname'] = boards[0].boardname
        res_data['boards'] = boards
        
    except Cfboard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'qna.html', res_data)

class BoardLV(ListView):
    model = Cfboard

class QnAView(TemplateView):

    template_name = 'qna.html'

    def get_context_data(self, **kwargs):
        context = super(QnAView, self).get_context_data(**kwargs)

        boardname = 3

        try:
            boards = Cfboard.objects.filter(boardname=boardname)
            context['boards'] = boards
            
        except Cfboard.DoesNotExist:
            pass
        
        return context