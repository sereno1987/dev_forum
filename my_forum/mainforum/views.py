
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Boards, Topics, Posts
from .forms import TopicForm, ReplyForm
from django.contrib.auth.decorators import login_required
import timeago
from django.db.models import Count


def home(request):
    boards = Boards.objects.all()
    posts = Posts.objects.all()
    return render(request, "index.html", {"boards": boards, "posts":posts})


def board_topics(request, pk):
    try:
        board = Boards.objects.get(pk=pk)
        topics=board.topics.order_by('-last_update').annotate(replies=Count('posts')-1)
        views=board.topics.order_by('-last_update').annotate(replies=Count('posts')-1)
        return render(request, "topic.html", {"boards": board , "topics":topics})
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
            return redirect('topic_posts', pk=board.pk ,topic_pk=topic.pk)
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
    topic.views +=1
    topic.save()
    converted_time=Topics.objects.get(pk=topic_pk).last_update
    created_at=timeago.format(converted_time, now())
    return render(request, "topic_posts.html", {"topics": topic, "created_at": created_at})


@login_required
def reply_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topics,  board__pk=pk, pk=topic_pk)
    converted_time = Topics.objects.get(pk=topic_pk).last_update
    created_at = timeago.format(converted_time, now())
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic= topic
            post.creator = request.user
            post.updated_by= request.user
            post.save()
            return redirect('topic_posts', pk=pk ,topic_pk=topic.pk)
    else:
        form = ReplyForm()
    return render(request, "reply_posts.html", {"topics": topic, "form": form,"created_at": created_at})
