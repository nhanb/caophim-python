from django.contrib import admin
from django.urls import path

from caophim_web import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.board_view, name="home"),
    path("<slug:board_id>/", views.board_view, name="board"),
    path(
        "<slug:board_id>/create-thread", views.create_thread_view, name="create-thread"
    ),
    path("<slug:board_id>/threads/<int:thread_id>/", views.thread_view, name="thread"),
    path(
        "<slug:board_id>/threads/<int:thread_id>/create-reply",
        views.create_reply_view,
        name="create-reply",
    ),
]
