from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Boards, Topics, Posts, User


def home(request):
    boards=Boards.objects.all()
    board_num=(Boards.objects.all().count())
    return render(request,"index.html", {"boards":boards, "board_num":board_num})


def board_topics(request,pk):
    try:
        board = Boards.objects.get(pk=pk)
        topic=Topics.objects
        return render(request,"topic.html", {"boards":board, "topics":topic})
    except Boards.DoesNotExist:
        raise Http404



def new_topics(request,pk):
    board = get_object_or_404(Boards, pk=pk)
    if request.method== "POST":
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        user=User.objects.first()

        topic=Topics.objects.create(
            subject=subject,
            board=board,
            creator=user
        )


        post=Posts.objects.create(
            message=message,
            topic=topic,
            creator=user
        )
        return  redirect('board_topics', pk=board.pk)

    return render(request,"newTopic.html", {"boards":board})