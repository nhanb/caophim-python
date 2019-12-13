from .models import Board


def get_boards(request, cache={}):
    if not cache:
        boards = Board.objects.all().order_by("id")
        cache["boards"] = boards
    return cache
