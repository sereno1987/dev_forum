from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Boards, Topics, Posts
# from django.shortcuts import get_object_or_404

def home(request):
    boards=Boards.objects.all()
    board_num=(Boards.objects.all().count())
    return render(request,"index.html", {"boards":boards, "board_num":board_num})


def board_topics(request,pk):
    try:
        boards = Boards.objects.get(pk=pk)
        topics=Topics.objects
        return render(request,"topic.html", {"boards":boards, "topics":topics})
    except Boards.DoesNotExist:
        raise Http404



def message_topics(request,pk):
    boards = get_object_or_404(Boards, pk=pk)
    return render(request,"newTopic.html", {"boards":boards})