from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Boards, Topics, Posts
from .forms import TopicForm


def home(request):
    boards = Boards.objects.all()
    board_num = (Boards.objects.all().count())
    return render(request, "index.html", {"boards": boards, "board_num": board_num})


def board_topics(request, pk):
    try:
        board = Boards.objects.get(pk=pk)
        return render(request, "topic.html", {"boards": board})
    except Boards.DoesNotExist:
        raise Http404

# using form API
def new_topics(request, pk):
    board = get_object_or_404(Boards, pk=pk)
    user = User.objects.first()
    if request.method == "POST":
        print("post")
        form=TopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            topic.creator=user
            topic.save()

            post=Posts.objects.create(
                message=form.cleaned_data.get('message'),
                creator= user,
                topic = topic,
                updated_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
         form=TopicForm()
    return render(request, "newTopic.html", {"boards": board, "form":form})



# without form API
# def new_topics(request, pk):
#     board = get_object_or_404(Boards, pk=pk)
#     if request.method == "POST":
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#
#         user = User.objects.first()
#
#         topic = Topics.objects.create(
#             subject=subject,
#             board=board,
#             creator=user
#         )
#
#         post = Posts.objects.create(
#             message=message,
#             topic=topic,
#             creator=user,
#             updated_by=user
#         )
#         return  redirect('board_topics', pk=board.pk)
#
#     return render(request, "newTopic.html", {"boards": board})
