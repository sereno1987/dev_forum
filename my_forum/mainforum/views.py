
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Boards, Topics, Posts
from .forms import TopicForm
from django.contrib.auth.decorators import login_required


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
@login_required
def new_topics(request, pk):
    board = get_object_or_404(Boards, pk=pk)
    if request.method == "POST":
        print("post")
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.creator = request.user
            topic.save()

            post = Posts.objects.create(
                message=form.cleaned_data.get('message'),
                creator=request.user,
                topic=topic,
                updated_by=request.user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = TopicForm()
    return render(request, "newTopic.html", {"boards": board, "form": form})


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
#             creator=request.user
#         )
#
#         post = Posts.objects.create(
#             message=message,
#             topic=topic,
#             creator=request.user,
#             updated_by=request.user
#         )
#         return  redirect('board_topics', pk=board.pk)
#
#     return render(request, "newTopic.html", {"boards": board})

# for posts
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topics,  board__pk=pk, pk=topic_pk)
    print("topic----------------------------------------------------")
    print(topic.subject)
    return render(request, "topic_posts.html", {"topics": topic})
