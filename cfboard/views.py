from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator

from cfboard.models import *
from cfuser.models import Cfuser

# Create your views here.
def index(request):
    return render(request, 'board.html')

def board_detail(request, pk, id):
    boardname = Boardcode.objects.get(id=pk)
    res_data = {'boardname' : boardname, 'pk' : pk, 'id' : id}
    try:
        board = Cfboard.objects.get(id=id)
        user = Cfuser.objects.get(id=board.writer.id)
        res_data['user'] = user
        res_data['board'] = board
        comments = Boardcomment.objects.filter(board=board)
        res_data['comments'] = comments
        board.hits = board.hits+1
        board.save()
    except Cfboard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')


    return render(request, 'cfboard/cfboard_detail.html', res_data)
    

def boards(request, pk):
    res_data = {'pk' : pk}
    boardname = Boardcode.objects.get(id=pk)
    if request.method=="POST":
        delete_id = request.POST.get('delete')
        delete_board = Cfboard.objects.filter(id=delete_id)
        if delete_board:
            delete_board.delete()
    try:
        board_lists = Cfboard.objects.filter(boardname=boardname).order_by('id')
        board_list = []
        for idx, board in enumerate(board_lists):
            board_list.append([idx+1,board])
        board_list.reverse()
        res_data['boardname'] = boardname
        res_data['boards'] = board_list
        paginator = Paginator(board_list, 8) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        res_data['page_obj'] = page_obj
        
    except Cfboard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'cfboard/cfboard.html', res_data)

def board_write(request, pk):
    errors = []
    boardname = Boardcode.objects.get(id=pk)
    catelist = Boardcate.objects.all()
    print('here',request)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        contents = request.POST.get('contents', '').strip()
        category = request.POST.get('category')
        disclosure = request.POST.get('disclosure')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not contents:
            errors.append('내용을 입력해주세요.')

        if not errors and 'user' in request.session:
            user = Cfuser.objects.get(email=request.session['user'])
            catename = Boardcate.objects.get(id=category)
            
            cfboard = Cfboard.objects.create(writer=user, title=title, contents=contents, catename=catename, boardname=boardname, hits=0, disclosure=disclosure)

            return redirect(reverse('cfboard:boards', kwargs={'pk': pk}))
    

    return render(request, 'cfboard/cfboard_write.html', {'errors':errors, 'pk':pk, 'catelist':catelist})


def comment_write(request, pk, id):
    errors = []
    if request.method == "POST":
        user = Cfuser.objects.get(email=request.session['user'])
        board = Cfboard.objects.get(id=id)
        contents = request.POST.get('contents')

        if not contents:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Boardcomment.objects.create(board=board, user=user, contents=contents)
            return redirect(reverse('cfboard:board_detail', kwargs={'pk': pk, 'id' : id}))

    return redirect(reverse('cfboard:board_detail', kwargs={'pk': pk, 'id' : id}))
    # return render(request, 'cfboard/cfboard_detail.html', {'board' : board, 'pk' : pk, 'id' : id,  'errors':errors})

