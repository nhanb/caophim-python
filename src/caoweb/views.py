from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from caoweb.forms import CreateReplyForm, CreateThreadForm
from caoweb.models import Board, Post


@require_GET
def board_view(request, board_id=None):
    if board_id is None:
        objects = Post.thread_objects
        create_thread_form = None
        title = "/ - tất cả"
        subtitle = ""
    else:
        board: Board = get_object_or_404(Board, id=board_id)
        objects = board.threads
        create_thread_form = CreateThreadForm(initial={"board": board})
        title = str(board)
        subtitle = board.description

    threads = (
        objects.all()
        .annotate(last_reply_created_at=Max("replies__created_at"))
        .order_by("-last_reply_created_at", "-id")
    )
    return render(
        request,
        "board.html",
        {
            "title": title,
            "subtitle": subtitle,
            "threads": threads,
            "create_thread_form": create_thread_form,
            "board_id": board_id,
        },
    )


@require_GET
def thread_view(request, board_id, thread_id):
    thread = get_object_or_404(
        Post.thread_objects.filter(board_id=board_id).select_related("board"),
        id=thread_id,
    )
    replies = thread.replies.all().order_by("id")
    create_reply_form = CreateReplyForm(initial={"parent_thread": thread})
    return render(
        request,
        "thread.html",
        {
            "title": str(thread.board),
            "subtitle": thread.board.description,
            "thread": thread,
            "replies": replies,
            "create_reply_form": create_reply_form,
            "board_id": board_id,
        },
    )


@require_POST
def create_thread_view(request, board_id):
    form = CreateThreadForm(request.POST)

    if not form.is_valid():
        return redirect("board", board_id=board_id)

    data = form.cleaned_data
    thread = Post.create_thread(data["board"].id, data["subject"], data["comment"])
    return redirect("thread", board_id=board_id, thread_id=thread.id)


@require_POST
def create_reply_view(request, board_id, thread_id):
    form = CreateReplyForm(request.POST)

    if not form.is_valid():
        return redirect("thread", board_id=board_id, thread_id=thread_id)

    data = form.cleaned_data
    reply = Post.create_reply(data["parent_thread"].id, data["comment"])
    return redirect(reply)
