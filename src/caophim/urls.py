from django.contrib import admin
from django.urls import path

from caoweb import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.board_view, name="home"),
    path("<board_id>/", views.board_view, name="board"),
    path("<board_id>/create-thread", views.create_thread_view, name="create-thread"),
    path("<board_id>/threads/<int:thread_id>/", views.thread_view, name="thread"),
    path(
        "<board_id>/threads/<int:thread_id>/create-reply",
        views.create_reply_view,
        name="create-reply",
    ),
]
